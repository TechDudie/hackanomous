<svelte:options runes={false} />

<script>
    import { onMount } from "svelte";

    import { gsap } from "gsap";
    import { ScrollTrigger } from "gsap/ScrollTrigger";

    export let left = "0dvw";
    export let placement = "top";
    export let date = "";
    export let title = "";
    export let description = "";
    export let href = "";
    export let scrollTween;

    /** @type {HTMLDivElement | undefined} */
    let eventEl;
    /** @type {HTMLDivElement | undefined} */
    let stemEl;
    /** @type {HTMLDivElement | undefined} */
    let cardEl;
    /** @type {gsap.core.Timeline | undefined} */
    let enterTimeline;

    $: isTop = placement === "top";
    $: stemClass = isTop ? "absolute bottom-0 left-0 w-[2px] h-[120px] bg-(--accent) origin-bottom rotate-[30deg]" : "absolute top-0 left-0 w-[2px] h-[120px] bg-(--accent) origin-top rotate-[-30deg]";
    $: cardClass = isTop ? "absolute bottom-[104px] left-[60px] w-[260px] border-b-2 border-(--accent) pb-4" : "absolute top-[104px] left-[60px] w-[260px] border-t-2 border-(--accent) pt-4";

    const destroyAnimation = () => {
        enterTimeline?.scrollTrigger?.kill();
        enterTimeline?.kill();
        enterTimeline = undefined;
    };

    const createAnimation = () => {
        if (!eventEl || !stemEl || !cardEl || !scrollTween) return;

        destroyAnimation();

        const startX = isTop ? -80 : 80;
        const startY = isTop ? -16 : 16;

        gsap.set([stemEl, cardEl], { autoAlpha: 0 });

        enterTimeline = gsap.timeline({
            defaults: { ease: "none" },
            scrollTrigger: {
                trigger: eventEl,
                containerAnimation: scrollTween,
                start: "left 96%",
                end: "left 62%",
                scrub: 0.35,
                invalidateOnRefresh: true,
            },
        });

        enterTimeline.fromTo(stemEl, { autoAlpha: 0, scaleY: 0, transformOrigin: isTop ? "bottom center" : "top center" }, { autoAlpha: 1, scaleY: 1, duration: 0.45 }).fromTo(cardEl, { autoAlpha: 0, x: startX, y: startY }, { autoAlpha: 1, x: 0, y: 0, duration: 0.4 }, 0.08);
    };

    onMount(() => {
        gsap.registerPlugin(ScrollTrigger);

        return () => {
            destroyAnimation();
        };
    });

    $: if (eventEl && stemEl && cardEl && scrollTween) {
        createAnimation();
    }
</script>

<div bind:this={eventEl} class="absolute top-1/2 group" style={`left: ${left};`}>
    <div bind:this={stemEl} class={stemClass}></div>
    <div bind:this={cardEl} class={cardClass}>
        <h4 class="font-mono text-2xl text-(--accent) font-semibold tracking-widest uppercase">{date}</h4>
        <h5 class="font-heading text-xl text-(--text) mt-3 leading-tight tracking-wide">{title}</h5>

        {#if href}
            <p class="font-content text-(--text-h) text-sm mt-2 opacity-80">
                <a {href} target="_blank" rel="noopener noreferrer" class="underline">{description}</a>
            </p>
        {:else}
            <p class="font-content text-(--text-h) text-sm mt-2 opacity-80">{description}</p>
        {/if}
    </div>
</div>
