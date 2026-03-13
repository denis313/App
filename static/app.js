(() => {
  const state = {
    audio: new Audio(),
    last: {
      src: null,
      key: null,
      score: null,
    },
    commands: [],
  };

  // iOS: keep in-page playback
  state.audio.playsInline = true;

  function normalizeKey(key) {
    return String(key || "")
      .trim()
      .toLowerCase()
      .replace(/\s+/g, "_");
  }

  function buildLocalAudioSrc(key) {
    return `/static/audio/${normalizeKey(key)}.mp3`;
  }

  function buildErrorAudioSrc(key, score) {
    const k = normalizeKey(key);
    const s = score == null ? "0" : String(score);
    return `/static/audio/errors/${k}_${s}.mp3`;
  }

  async function playSrc(src, meta) {
    try {
      state.audio.pause();
      state.audio.currentTime = 0;
    } catch (_) {}

    state.audio.src = src;
    state.audio.load();

    try {
      await state.audio.play();
      state.last.src = src;
      state.last.key = meta?.key ?? state.last.key;
      state.last.score = meta?.score ?? state.last.score;
    } catch (e) {
      console.warn("Audio play blocked/failed:", e);
    }
  }

  function stopAudio() {
    try {
      state.audio.pause();
      state.audio.currentTime = 0;
    } catch (_) {}
  }

  async function playByKey(key, score = null) {
    const src = buildLocalAudioSrc(key);
    await playSrc(src, { key, score });
  }

  async function playCommand(cmd) {
    // cmd.path can be absolute URL, absolute path, or relative path.
    const p = String(cmd.path || "").trim();
    const src = p.startsWith("http://") || p.startsWith("https://") || p.startsWith("/")
      ? p
      : `/${p}`;
    await playSrc(src, { key: cmd.name, score: null });
  }

  async function repeatLast() {
    if (!state.last.src) return;
    await playSrc(state.last.src, { key: state.last.key, score: state.last.score });
  }

  async function playError() {
    if (!state.last.key) return;
    const src = buildErrorAudioSrc(state.last.key, state.last.score);
    await playSrc(src, { key: state.last.key, score: state.last.score });
  }

  // Modal for commands list
  const modal = document.getElementById("commandsModal");
  const modalList = document.getElementById("commandsList");
  const modalClose = document.getElementById("commandsClose");

  function openCommandsModal() {
    modal?.classList.add("open");
  }
  function closeCommandsModal() {
    modal?.classList.remove("open");
  }

  async function loadCommands() {
    const res = await fetch("/api/commands", { headers: { "Accept": "application/json" } });
    if (!res.ok) throw new Error(`Commands load failed: ${res.status}`);
    state.commands = await res.json();
  }

  function renderCommands() {
    if (!modalList) return;
    modalList.innerHTML = "";

    const items = Array.isArray(state.commands) ? state.commands : [];
    if (!items.length) {
      const empty = document.createElement("div");
      empty.className = "commands-empty";
      empty.textContent = "Команды не найдены";
      modalList.appendChild(empty);
      return;
    }

    for (const cmd of items) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "commands-item pressable pressable-scale";
      btn.textContent = cmd.name;
      btn.addEventListener("click", () => playCommand(cmd));
      modalList.appendChild(btn);
    }
  }

  async function showCommands() {
    try {
      await loadCommands();
    } catch (e) {
      console.warn(e);
      state.commands = [];
    }
    renderCommands();
    openCommandsModal();
  }

  function bindPlayableButton(id, key, score = null) {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener("click", () => playByKey(key, score));
  }

  // Bind main UI buttons to local audio (EXCEPT commands/errors)
  bindPlayableButton("btnForward", "вперед");
  bindPlayableButton("btnLeft", "налево_на_перекрестке");
  bindPlayableButton("btnRight", "направо_на_перекрестке");
  bindPlayableButton("btnUTurnCross", "разворот_на_перекрестке");
  bindPlayableButton("btnUTurnNoCross", "разворот_вне_перекрестка");
  bindPlayableButton("btnParking", "парковка");

  // Center repeat button
  document.getElementById("btnRepeat")?.addEventListener("click", () => repeatLast());

  // Cancel stops playback
  document.getElementById("btnCancel")?.addEventListener("click", () => stopAudio());

  // Ring exits (sectors 1-5)
  document.querySelectorAll(".sector").forEach((el) => {
    el.addEventListener("click", () => {
      const n = Number(el.dataset.sector);
      const score = Number.isFinite(n) ? n : null;
      playByKey(`съезд_${score}`, score);
    });
  });

  // Commands / Errors behavior
  document.getElementById("btnCommands")?.addEventListener("click", () => showCommands());
  document.getElementById("btnErrors")?.addEventListener("click", () => playError());

  // Modal close handlers
  modalClose?.addEventListener("click", () => closeCommandsModal());
  modal?.addEventListener("click", (e) => {
    if (e.target === modal) closeCommandsModal();
  });
})();

