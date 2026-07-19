"""Shared build-time layout rules for both standalone HTML generators."""

SIDEBAR_COLLAPSE_WIDTH = 1300
SIDEBAR_MEDIA_QUERY = f"(max-width: {SIDEBAR_COLLAPSE_WIDTH}px)"


_COMMON_LAYOUT_CSS = """
<style data-responsive-layout-system="true">
    :root {
        --layout-vh: 100vh;
        --layout-sidebar-width: 300px;
        --layout-gutter: clamp(20px, 2.5vw, 80px);
        --layout-main-start: calc(var(--layout-sidebar-width) + 20px);
        --layout-main-end: clamp(20px, 5.55vw, 80px);
        --layout-block-space: clamp(70px, 8.9vh, 80px);
        --layout-focus-space: clamp(20px, 5vh, 40px);
        --layout-control-edge: clamp(12px, 1.4vw, 20px);
        --layout-control-width: clamp(80px, 8.333vw, 120px);
        --layout-control-padding-y: clamp(6px, 0.7vw, 8px);
        --layout-control-padding-x: clamp(12px, 1.25vw, 18px);
        --layout-card-padding-block: clamp(20px, 2.8vw, 40px);
        --layout-card-padding-inline: clamp(15px, 2.1vw, 30px);
        --layout-gap: clamp(10px, 1.4vw, 20px);
        --motion-fast: 160ms;
        --motion-layout: 260ms;
        --motion-ease: cubic-bezier(.2, .8, .2, 1);
    }

    @supports (height: 100dvh) {
        :root { --layout-vh: 100dvh; }
    }

    html,
    body {
        min-width: 0;
        min-height: 100vh;
        min-height: var(--layout-vh);
        overflow-x: clip;
    }

    .top-toolbar {
        position: fixed;
        inset: 0 0 auto 0;
        height: calc(var(--layout-control-edge) + 48px);
        z-index: 20;
        pointer-events: none;
    }

    .top-toolbar .btn-float {
        position: absolute;
        top: var(--layout-control-edge);
        width: var(--layout-control-width);
        padding: var(--layout-control-padding-y) var(--layout-control-padding-x);
        font-size: clamp(10px, 1.1vw, 16px);
        white-space: nowrap;
        pointer-events: auto;
    }

    .top-toolbar .btn-menu {
        left: var(--layout-control-edge);
        display: flex;
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        transform: scale(.96);
        transition:
            opacity var(--motion-layout) var(--motion-ease),
            transform var(--motion-layout) var(--motion-ease),
            visibility 0s linear var(--motion-layout);
    }

    .top-toolbar .btn-focus {
        left: 50%;
        transform: translateX(-50%);
    }

    .top-toolbar .btn-focus:hover {
        transform: translateX(-50%) scale(1.05);
    }

    .top-toolbar .btn-theme {
        right: var(--layout-control-edge);
    }

    .btn-list {
        right: var(--layout-control-edge);
        bottom: var(--layout-control-edge);
        width: var(--layout-control-width);
        padding: var(--layout-control-padding-y) var(--layout-control-padding-x);
        font-size: clamp(10px, 1.1vw, 16px);
        white-space: nowrap;
    }

    .btn {
        transition:
            transform var(--motion-fast) var(--motion-ease),
            opacity var(--motion-fast) var(--motion-ease),
            background-color var(--motion-fast) var(--motion-ease),
            color var(--motion-fast) var(--motion-ease),
            box-shadow var(--motion-fast) var(--motion-ease);
    }

    .sidebar {
        width: var(--layout-sidebar-width);
        height: 100vh;
        height: var(--layout-vh);
        box-sizing: border-box;
        transform: translateX(0);
        transition: transform var(--motion-layout) var(--motion-ease);
    }

    .sidebar-container {
        transition: transform var(--motion-layout) var(--motion-ease);
    }

    .main {
        top: var(--layout-block-space);
        bottom: var(--layout-block-space);
        left: var(--layout-main-start);
        right: var(--layout-main-end);
        min-width: 0;
        min-height: 0;
        transition:
            top var(--motion-layout) var(--motion-ease),
            bottom var(--motion-layout) var(--motion-ease),
            left var(--motion-layout) var(--motion-ease),
            right var(--motion-layout) var(--motion-ease);
    }

    .main > .card {
        max-height: 100%;
        min-width: 0;
        box-sizing: border-box;
        transition:
            width var(--motion-layout) var(--motion-ease),
            height var(--motion-layout) var(--motion-ease),
            min-height var(--motion-layout) var(--motion-ease),
            max-width var(--motion-layout) var(--motion-ease),
            padding var(--motion-layout) var(--motion-ease);
    }

    body.focus-mode .main {
        top: var(--layout-focus-space);
        bottom: var(--layout-focus-space);
        left: 5px;
        right: 5px;
    }

    .modal-content {
        width: min(90vw, 1200px);
        top: var(--layout-block-space);
        bottom: var(--layout-block-space);
        max-height: calc(var(--layout-vh) - 2 * var(--layout-block-space));
        box-sizing: border-box;
    }

    @media (max-width: __SIDEBAR_BREAKPOINT__px) {
        :root {
            --layout-main-start: var(--layout-gutter);
            --layout-main-end: var(--layout-gutter);
        }

        .sidebar {
            width: min(280px, calc(100vw - 40px));
            transform: translateX(-100%);
        }

        .sidebar.mobile-open {
            transform: translateX(0);
        }

        .top-toolbar .btn-menu {
            opacity: 1;
            visibility: visible;
            pointer-events: auto;
            transform: scale(1);
            transition:
                opacity var(--motion-layout) var(--motion-ease),
                transform var(--motion-layout) var(--motion-ease),
                visibility 0s linear 0s;
        }

        .sidebar.mobile-open ~ .main {
            left: var(--layout-main-start);
        }
    }

    @media (max-width: 840px) {
        :root {
            --layout-gutter: clamp(12px, 4vw, 20px);
        }

        .modal-content {
            width: calc(100vw - 2 * var(--layout-gutter));
        }

        .modal-body {
            grid-template-columns: 1fr;
        }
    }

    @media (max-height: 700px) {
        :root {
            --layout-block-space: clamp(56px, 10vh, 70px);
            --layout-focus-space: clamp(10px, 3vh, 20px);
            --layout-card-padding-block: clamp(12px, 3vh, 20px);
            --layout-gap: clamp(8px, 2vh, 12px);
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            scroll-behavior: auto !important;
            animation-duration: 0s !important;
            animation-delay: 0s !important;
            transition-duration: 0s !important;
            transition-delay: 0s !important;
        }

        ::view-transition-old(*),
        ::view-transition-new(*) {
            animation-duration: 0s !important;
        }
    }

__PAGE_RULES__
</style>
"""


_PAGE_RULES = {
    "word-list": """
    .main > .card {
        width: 100%;
        max-width: 800px;
        height: auto;
        min-height: min(400px, 100%);
        padding: var(--layout-card-padding-block) var(--layout-card-padding-inline);
        overflow: hidden;
    }

    .card-header {
        margin-bottom: clamp(15px, 2.1vw, 30px);
        gap: var(--layout-gap);
    }

    .counter {
        min-width: clamp(80px, 8.3vw, 120px);
    }

    .word {
        font-size: clamp(2rem, 5vw, 4.5rem);
    }

    .definition-area {
        min-height: clamp(120px, 20vh, 180px);
        min-height: clamp(120px, 20dvh, 180px);
        margin: 0 0 clamp(10px, 1.4vw, 15px);
    }

    .definition {
        font-size: clamp(1.2rem, 2.5vw, 1.8rem);
    }

    .card-actions {
        gap: var(--layout-gap);
    }

    .card-actions .btn {
        min-width: clamp(70px, 7vw, 100px);
        padding: clamp(10px, 1vw, 12px) clamp(12px, 1.75vw, 25px);
        font-size: clamp(12px, 1.25vw, 18px);
    }

    body.focus-mode .card {
        min-height: 0;
        height: 100%;
        padding: clamp(15px, 3vh, 30px) clamp(10px, 2vw, 30px);
    }

    body.focus-mode .card-actions {
        padding-top: clamp(12px, 4vh, 40px);
        gap: var(--layout-gap);
    }

    body.focus-mode .card-actions .btn {
        min-width: clamp(70px, 14vw, 200px);
        padding: clamp(10px, 2vh, 20px) clamp(12px, 2vw, 30px);
        font-size: clamp(12px, 1.7vw, 24px);
        margin: 0 clamp(0px, .7vw, 10px);
    }

    """,
    "matching-game": """
    .main > .card {
        width: 100%;
        max-width: 1200px;
        height: 100%;
        min-height: 0;
        padding: clamp(12px, 3.3vh, 30px) 5px 0;
        overflow: hidden;
    }

    .card-header {
        margin-bottom: clamp(10px, 2.2vh, 20px);
        gap: var(--layout-gap);
    }

    .matching-area {
        min-height: 0;
        gap: var(--layout-gap);
        padding: clamp(8px, 1.7vh, 15px) 0 0;
    }

    .word-column,
    .definition-column {
        min-width: 0;
        min-height: 0;
        gap: clamp(8px, 1.2vw, 12px);
    }

    .word-card,
    .definition-card {
        min-width: 0;
        min-height: 0;
        padding: clamp(8px, 1vw, 15px) clamp(6px, .7vw, 10px);
        font-size: clamp(1rem, 2vw, 1.8rem);
        transition:
            transform var(--motion-fast) var(--motion-ease),
            opacity var(--motion-fast) var(--motion-ease),
            background-color var(--motion-fast) var(--motion-ease),
            border-color var(--motion-fast) var(--motion-ease);
    }

    @media (max-width: 840px) {
        .word-column,
        .definition-column { gap: 8px; }
        .matching-area { gap: 10px; }
    }
    """,
}


def render_responsive_layout_style(page_kind: str) -> str:
    """Return the shared embedded style block for a generated page."""
    if page_kind not in _PAGE_RULES:
        raise ValueError(f"Unsupported page kind: {page_kind}")

    return (
        _COMMON_LAYOUT_CSS.replace("__PAGE_RULES__", _PAGE_RULES[page_kind].strip())
        .replace("__SIDEBAR_BREAKPOINT__", str(SIDEBAR_COLLAPSE_WIDTH))
    )

