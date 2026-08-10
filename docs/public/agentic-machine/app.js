const visual = document.querySelector("#machine-visual");
const components = Array.from(document.querySelectorAll("[data-component]"));
const playButton = document.querySelector("#play-machine");
const restartButton = document.querySelector("#restart-machine");
const diagramPanel = document.querySelector("#diagram-panel");
const diagramViewport = document.querySelector("#diagram-viewport");
const noteTitle = document.querySelector("#diagram-title");
const noteText = document.querySelector("#diagram-summary");
const noteEyebrow = document.querySelector("#diagram-eyebrow");
const stepFeed = document.querySelector("#step-feed");

const overview = {
  eyebrow: "Overview",
  title: "The machine in one read",
  text:
    "Studio is the control room. Connectors and Knowledge supply what the agent can do and know. Compass, Versioning, Guardian, Proving Ground, Deploy, Traces, and Analytics turn that design into a safer customer-facing product loop.",
};

const explanations = {
  studio: {
    title: "Agent Studio",
    text: "Compose agents, skills, instructions, and tool access.",
  },
  connectors: {
    title: "Agentic Connectors",
    text: "Turn external system capabilities into agent-ready tools.",
  },
  marketplace: {
    title: "Marketplace / App Hub",
    text: "Discover and add supported connectors.",
  },
  byo: {
    title: "BYO MCP",
    text: "Bring a custom MCP connection into the same tool pipeline.",
  },
  registry: {
    title: "MCP Registry",
    text: "Hold the registered connector capabilities.",
  },
  catalog: {
    title: "Tool Catalog",
    text: "Make available tools visible for use in Studio.",
  },
  graph: {
    title: "AgentGraph",
    text: "Turn the designed agent into an executable runtime plan.",
  },
  proving: {
    title: "Proving Ground",
    text: "Test agent behavior and tool calls before release.",
  },
  analytics: {
    title: "Traces + Analytics",
    text: "Explain what happened and reveal where to improve.",
  },
  products: {
    title: "Customer experiences",
    text: "Voice includes AI Receptionist and AI Routing. Digital includes Digital Agent.",
  },
  "skill-mining": {
    title: "Skill Mining",
    text: "Surface processes that may be worth automating.",
  },
  "knowledge-studio": {
    title: "Knowledge Studio",
    text: "Prepare approved knowledge and grounding the agent can use.",
  },
  templates: {
    title: "Templates",
    text: "Give designers reusable starting points for common agent and skill patterns.",
  },
  composer: {
    title: "Composer",
    text: "Helps create and edit the agent instructions, skills, and configuration.",
  },
  skills: {
    title: "Skills",
    text: "Package specific jobs the agent can perform for a customer.",
  },
  "transfer-setup": {
    title: "Transfer setup",
    text: "Defines how the agent hands off to people, queues, channels, or other agents.",
  },
  compass: {
    title: "Compass",
    text: "Checks and improves the agent design before it moves deeper into testing.",
  },
  versioning: {
    title: "Versioning",
    text: "Locks drafts, tested versions, live releases, changelogs, and rollback points.",
  },
  workflows: {
    title: "Workflows",
    text: "Let runtime execution call structured business processes when a skill needs them.",
  },
  transfers: {
    title: "Transfers",
    text: "Move the interaction to the right human, destination, or agent path at runtime.",
  },
  context: {
    title: "Context variables",
    text: "Carry structured information through steps, branches, and handoffs.",
  },
  guardian: {
    title: "Guardian",
    text: "Protects live conversations from unsafe, policy-breaking, or unwanted behavior.",
  },
  "voice-test": {
    title: "Voice Test",
    text: "Lets teams try the agent as a voice experience before release.",
  },
  "mock-tools": {
    title: "Mock tools",
    text: "Let tests exercise connector behavior without writing to production systems.",
  },
  deploy: {
    title: "Deploy / Publish",
    text: "Moves a tested version into the customer-facing channel.",
  },
  history: {
    title: "History",
    text: "Shows the conversations and sessions teams review after release.",
  },
  traces: {
    title: "Traces",
    text: "Expose what the agent said, did, and reasoned through in a specific interaction.",
  },
  "ai-events": {
    title: "AI events",
    text: "Capture the important runtime events that explain behavior and outcomes.",
  },
  annotations: {
    title: "Issue clusters",
    text: "Group repeated failures or improvement opportunities so teams know what to fix next.",
  },
};

const relatedComponents = {
  studio: ["connectors", "catalog", "graph", "skill-mining", "knowledge-studio", "templates", "composer", "skills", "transfer-setup", "compass", "versioning"],
  connectors: ["marketplace", "byo", "registry", "catalog", "studio"],
  marketplace: ["connectors", "registry", "catalog"],
  byo: ["connectors", "registry", "catalog"],
  registry: ["connectors", "marketplace", "byo", "catalog"],
  catalog: ["connectors", "registry", "studio"],
  templates: ["studio", "composer", "skills"],
  composer: ["studio", "templates", "skills", "compass"],
  skills: ["studio", "templates", "workflows", "transfers", "context"],
  "transfer-setup": ["studio", "transfers", "context"],
  compass: ["studio", "composer", "skills", "versioning", "graph"],
  versioning: ["studio", "compass", "proving", "deploy", "analytics"],
  graph: ["studio", "compass", "workflows", "transfers", "context", "guardian", "proving", "products"],
  workflows: ["graph", "skills", "context"],
  transfers: ["graph", "transfer-setup", "context", "products"],
  context: ["graph", "transfers", "workflows", "analytics"],
  guardian: ["graph", "products", "traces", "analytics"],
  proving: ["graph", "voice-test", "mock-tools", "deploy", "analytics"],
  "voice-test": ["studio", "proving"],
  "mock-tools": ["connectors", "proving"],
  deploy: ["versioning", "proving", "products", "analytics"],
  analytics: ["products", "studio", "proving", "knowledge-studio", "history", "traces", "ai-events", "annotations"],
  history: ["analytics", "traces", "ai-events"],
  traces: ["analytics", "history", "guardian", "annotations"],
  "ai-events": ["analytics", "history", "traces"],
  annotations: ["analytics", "traces", "skill-mining", "studio"],
  products: ["graph", "guardian", "deploy", "analytics"],
  "skill-mining": ["studio", "knowledge-studio"],
  "knowledge-studio": ["studio", "analytics", "skill-mining"],
};

const componentStepMap = {
  connectors: 0,
  marketplace: 1,
  byo: 1,
  registry: 2,
  catalog: 3,
  studio: 7,
  "skill-mining": 5,
  "knowledge-studio": 6,
  templates: 7,
  composer: 7,
  skills: 7,
  "transfer-setup": 7,
  compass: 8,
  versioning: 9,
  graph: 11,
  workflows: 11,
  transfers: 11,
  context: 11,
  guardian: 12,
  proving: 14,
  "voice-test": 13,
  "mock-tools": 13,
  deploy: 15,
  products: 16,
  analytics: 17,
  history: 17,
  traces: 17,
  "ai-events": 17,
  annotations: 18,
};

let selectedComponent = null;
let playTimer = null;
let playState = "idle";
let currentPlayStepIndex = -1;

const stepDuration = 3600;

const setNote = (content) => {
  noteEyebrow.textContent = content.eyebrow || "Selected component";
  noteTitle.textContent = content.title;
  noteText.textContent = content.text;
};

const scrollToSvgY = (svgY) => {
  const viewBox = visual.viewBox.baseVal;
  const svgRect = visual.getBoundingClientRect();
  if (!viewBox.height || svgRect.height <= 0 || !diagramViewport) return;

  const viewportRect = diagramViewport.getBoundingClientRect();
  const yInSvg = (svgY / viewBox.height) * svgRect.height;
  const yInViewport = svgRect.top - viewportRect.top + diagramViewport.scrollTop + yInSvg;
  const targetY = Math.max(0, yInViewport - diagramViewport.clientHeight * 0.34);
  diagramViewport.scrollTo({ top: targetY, behavior: "smooth" });
};

const clearSelection = () => {
  selectedComponent = null;
  visual.classList.remove("has-selection");
  components.forEach((component) => {
    component.classList.remove("is-selected", "is-related");
  });
  setNote(overview);
};

const selectComponent = (componentName) => {
  if (selectedComponent === componentName) {
    clearSelection();
    clearPlayState();
    return;
  }

  const explanation = explanations[componentName];
  if (!explanation) return;

  clearPlayTimer();
  playState = "paused";
  visual.classList.add("is-paused");
  updatePlayButton();

  selectedComponent = componentName;
  const related = new Set(relatedComponents[componentName] || []);
  visual.classList.add("has-selection");

  components.forEach((component) => {
    const name = component.dataset.component;
    component.classList.toggle("is-selected", name === componentName);
    component.classList.toggle("is-related", name !== componentName && related.has(name));
  });

  const stepIndex = componentStepMap[componentName];
  const step = playSteps[stepIndex];

  if (step) {
    setPlayStep(step, stepIndex, {
      eyebrow: "Selected component",
    });
  } else {
    setNote({
      eyebrow: "Selected component",
      title: explanation.title,
      text: explanation.text,
    });
  }
};

components.forEach((component) => {
  component.addEventListener("click", (event) => {
    event.stopPropagation();
    selectComponent(component.dataset.component);
  });

  component.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      selectComponent(component.dataset.component);
    }
  });
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    clearSelection();
  }
});

const clearPlayTimer = () => {
  if (playTimer) {
    window.clearTimeout(playTimer);
    playTimer = null;
  }
};

const clearPlayHighlights = () => {
  document.querySelectorAll(".play-lit").forEach((element) => {
    element.classList.remove("play-lit");
  });
  document.querySelectorAll(".pulse-active").forEach((element) => {
    element.classList.remove("pulse-active");
  });
};

const updateFeedState = (activeIndex) => {
  const cards = Array.from(document.querySelectorAll(".feed-card"));
  cards.forEach((card, index) => {
    const isActive = index === activeIndex;
    card.classList.toggle("is-active", isActive);
    card.classList.toggle("is-paused", isActive && playState === "paused");
    if (isActive) {
      card.setAttribute("aria-current", "step");
      card.querySelector(".feed-state").textContent = "";
    } else {
      card.removeAttribute("aria-current");
      card.querySelector(".feed-state").textContent = "";
    }
  });

  const activeCard = cards[activeIndex];
  if (activeCard) {
    activeCard.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }
};

const updatePlayButton = () => {
  playButton.classList.toggle("is-paused", playState === "paused");
  playButton.setAttribute("aria-pressed", playState === "idle" ? "false" : "true");

  if (playState === "playing") {
    playButton.textContent = "Pause";
  } else if (playState === "paused") {
    playButton.textContent = "Resume";
  } else {
    playButton.textContent = "Play";
  }
};

const clearPlayState = ({ showOverview = true } = {}) => {
  clearPlayTimer();
  playState = "idle";
  currentPlayStepIndex = -1;
  visual.classList.remove("is-paused");
  clearPlayHighlights();
  updateFeedState(-1);
  updatePlayButton();

  if (showOverview) {
    setNote(overview);
  }
};

const setPlayStep = (step, index, { eyebrow = "Playing" } = {}) => {
  clearPlayHighlights();
  currentPlayStepIndex = index;

  step.active.forEach((name) => {
    document.querySelectorAll(`[data-component="${name}"], [data-play="${name}"]`).forEach((element) => {
      element.classList.add("play-lit");
    });
  });

  step.pulses.forEach((name) => {
    document.querySelectorAll(`[data-pulse="${name}"]`).forEach((element) => {
      element.classList.add("pulse-active");
    });
  });

  setNote({
    eyebrow,
    title: step.title,
    text: step.text,
  });
  updateFeedState(index);

  if (Number.isFinite(step.scrollY)) {
    scrollToSvgY(step.scrollY);
  }
};

const playSteps = [
  {
    active: ["sources"],
    pulses: ["sources"],
    scrollY: 150,
    title: "Customer systems become agent tools",
    text: "Customer systems get connected through Agentic Connectors so their capabilities become tools an agent can use in Agent Studio.",
  },
  {
    active: ["marketplace", "byo"],
    pulses: ["sources"],
    scrollY: 360,
    title: "There are two ways into the connector pipe",
    text: "Marketplace / App Hub is the prebuilt path, and BYO MCP is the custom path for customer-provided connectors.",
  },
  {
    active: ["registry", "connectors"],
    pulses: ["merge"],
    scrollY: 430,
    title: "Both paths merge into the MCP Registry",
    text: "The MCP Registry is where those connector capabilities become known to the agentic system.",
  },
  {
    active: ["catalog", "connectors"],
    pulses: ["catalog"],
    scrollY: 430,
    title: "The Tool Catalog makes the capabilities usable",
    text: "The Tool Catalog is the menu of actions that Agent Studio can expose to a designer.",
  },
  {
    active: ["studio", "connectors", "catalog"],
    pulses: ["tools"],
    scrollY: 790,
    title: "Tools enter Agent Studio",
    text: "The connector pipe delivers available tools into Agent Studio, where the designer chooses what the agent can use.",
  },
  {
    active: ["skill-mining", "studio"],
    pulses: [],
    scrollY: 700,
    title: "Skill Mining suggests what to automate",
    text: "Skill Mining helps teams spot repeated customer work that may be worth turning into an agent skill.",
  },
  {
    active: ["knowledge-studio", "studio"],
    pulses: ["knowledge"],
    scrollY: 700,
    title: "Knowledge Studio grounds what the agent knows",
    text: "Knowledge Studio supplies approved knowledge separately from connector tools, so the agent can answer with trusted context.",
  },
  {
    active: ["templates", "composer", "skills", "transfer-setup", "studio"],
    pulses: [],
    scrollY: 900,
    title: "Studio assembles the agent",
    text: "Templates, Composer, skills, tool access, and transfer setup all live around the Studio build experience.",
  },
  {
    active: ["compass", "studio", "skills", "composer"],
    pulses: ["plan"],
    scrollY: 1035,
    title: "Compass checks the design",
    text: "Compass is the pre-flight quality pass that helps catch weak instructions before testing and release.",
  },
  {
    active: ["versioning", "studio"],
    pulses: [],
    scrollY: 850,
    title: "Versioning locks what changed",
    text: "Versioning keeps draft, tested, and live agent versions traceable so teams can compare, publish, and roll back.",
  },
  {
    active: ["studio", "graph", "compass"],
    pulses: ["plan"],
    scrollY: 1080,
    title: "Studio sends the design to AgentGraph",
    text: "Agent Studio is where the agent is composed; AgentGraph turns that design into something that can run.",
  },
  {
    active: ["graph", "workflows", "transfers", "context"],
    pulses: ["plan"],
    scrollY: 1200,
    title: "AgentGraph runs the agent",
    text: "AgentGraph executes steps, workflows, transfers, context variables, branches, and tool calls.",
  },
  {
    active: ["guardian", "graph"],
    pulses: ["plan"],
    scrollY: 1200,
    title: "Guardian protects runtime behavior",
    text: "Guardian sits with runtime execution so unsafe or policy-breaking behavior can be caught during live conversations.",
  },
  {
    active: ["voice-test", "mock-tools", "proving"],
    pulses: ["proving"],
    scrollY: 1480,
    title: "Voice Test and mock tools reduce risk",
    text: "Voice Test lets teams try the agent experience, while mock tools prevent tests from writing into production systems.",
  },
  {
    active: ["proving", "graph", "mock-tools"],
    pulses: ["proving"],
    scrollY: 1460,
    title: "Proving Ground tests before release",
    text: "Proving Ground lets teams test behavior and tool use safely before the agent reaches customers.",
  },
  {
    active: ["deploy", "versioning", "proving", "products"],
    pulses: ["release"],
    scrollY: 1648,
    title: "Deploy publishes a tested version",
    text: "Deploy / Publish moves the approved version into the customer-facing voice or digital channel.",
  },
  {
    active: ["products", "deploy", "guardian"],
    pulses: ["release"],
    scrollY: 2060,
    title: "Products deliver the experience",
    text: "Voice products include AI Receptionist and AI Routing. Digital Agent covers digital channels.",
  },
  {
    active: ["analytics", "history", "traces", "ai-events"],
    pulses: ["telemetry"],
    scrollY: 1810,
    title: "History, Traces, and Analytics explain it",
    text: "History, Traces, AI events, and Analytics show what happened, why it happened, and whether it worked.",
  },
  {
    active: ["analytics", "annotations", "skill-mining"],
    pulses: ["telemetry"],
    scrollY: 1810,
    title: "Issue clusters reveal what to fix",
    text: "Annotations and issue clusters turn repeated failures into a focused list of improvements.",
  },
  {
    active: ["analytics", "studio", "versioning", "skill-mining", "feedback"],
    pulses: ["feedback"],
    scrollY: 1260,
    title: "Learning feeds the next version",
    text: "Teams use production learning, Skill Mining, and version history to improve the next agent version in Studio.",
  },
];

const renderStepFeed = () => {
  stepFeed.innerHTML = "";

  playSteps.forEach((step, index) => {
    const item = document.createElement("li");
    item.className = "feed-item";

    const button = document.createElement("button");
    button.className = "feed-card";
    button.type = "button";
    button.dataset.stepIndex = String(index);
    button.setAttribute("aria-label", `${step.title}`);

    const body = document.createElement("span");
    const state = document.createElement("span");
    state.className = "feed-state";
    state.textContent = "";

    const title = document.createElement("span");
    title.className = "feed-title";
    title.textContent = step.title;

    const text = document.createElement("span");
    text.className = "feed-text";
    text.textContent = step.text;

    body.append(state, title, text);
    button.append(body);
    item.append(button);
    stepFeed.append(item);

    button.addEventListener("click", () => {
      jumpToStep(index);
    });
  });
};

const jumpToStep = (index) => {
  const step = playSteps[index];
  if (!step) return;

  clearSelection();
  clearPlayTimer();
  playState = "paused";
  visual.classList.add("is-paused");
  updatePlayButton();
  setPlayStep(step, index, {
    eyebrow: "Selected",
  });
};

const scheduleNextPlayStep = () => {
  clearPlayTimer();
  playTimer = window.setTimeout(() => {
    if (playState !== "playing") return;

    const nextIndex = currentPlayStepIndex + 1;
    if (nextIndex >= playSteps.length) {
      clearPlayState();
      return;
    }

    setPlayStep(playSteps[nextIndex], nextIndex);
    scheduleNextPlayStep();
  }, stepDuration);
};

const startPlay = () => {
  clearSelection();
  clearPlayState({ showOverview: false });
  playState = "playing";
  visual.classList.remove("is-paused");
  updatePlayButton();
  setPlayStep(playSteps[0], 0);
  scheduleNextPlayStep();
};

const pausePlay = () => {
  if (playState !== "playing") return;

  clearPlayTimer();
  playState = "paused";
  visual.classList.add("is-paused");
  updatePlayButton();

  const currentStep = playSteps[currentPlayStepIndex];
  if (currentStep) {
    setNote({
      eyebrow: "Paused",
      title: currentStep.title,
      text: `Paused here. ${currentStep.text}`,
    });
    updateFeedState(currentPlayStepIndex);
  }
};

const resumePlay = () => {
  if (playState !== "paused") return;

  playState = "playing";
  visual.classList.remove("is-paused");
  updatePlayButton();

  const currentStep = playSteps[currentPlayStepIndex];
  if (currentStep) {
    setNote({
      eyebrow: "Playing",
      title: currentStep.title,
      text: currentStep.text,
    });
    updateFeedState(currentPlayStepIndex);
  }

  scheduleNextPlayStep();
};

const restartPlay = () => {
  clearSelection();
  clearPlayState({ showOverview: false });
  playState = "playing";
  visual.classList.remove("is-paused");
  updatePlayButton();
  if (diagramViewport) {
    diagramViewport.scrollTo({ top: 0, behavior: "smooth" });
  }
  setPlayStep(playSteps[0], 0);
  scheduleNextPlayStep();
};

playButton.addEventListener("click", () => {
  if (playState === "playing") {
    pausePlay();
  } else if (playState === "paused") {
    resumePlay();
  } else {
    startPlay();
  }
});

restartButton.addEventListener("click", restartPlay);

diagramPanel.addEventListener("click", (event) => {
  if (
    event.target.closest("button") ||
    event.target.closest("[data-component]")
  ) {
    return;
  }

  if (playState === "playing") {
    pausePlay();
  } else if (playState === "paused") {
    resumePlay();
  } else {
    startPlay();
  }
});

renderStepFeed();
updatePlayButton();
setNote(overview);
