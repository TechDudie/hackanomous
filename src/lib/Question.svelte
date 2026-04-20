<script>
    import { cubicOut } from "svelte/easing";

    let { question, children } = $props();
    let isOpen = $state(false);

    /**
     * @param {Element} node
     */
    function angledSlide(node, { duration = 400 }) {
        const style = getComputedStyle(node);
        const height = parseFloat(style.height);
        const paddingTop = parseFloat(style.paddingTop);
        const paddingBottom = parseFloat(style.paddingBottom);
        const marginTop = parseFloat(style.marginTop);
        const marginBottom = parseFloat(style.marginBottom);

        return {
            duration,
            easing: cubicOut,
            css: (/** @type {number} */ t) => {
                const currentHeight = t * height;
                return `
                    overflow: hidden;
                    height: ${currentHeight}px;
                    padding-top: ${t * paddingTop}px;
                    padding-bottom: ${t * paddingBottom}px;
                    margin-top: ${t * marginTop}px;
                    margin-bottom: ${t * marginBottom}px;
                    clip-path: polygon(
                        0 0,
                        ${t * 100}% 0,
                        ${t * 100}% calc(${t * 100}% - ${t * 20}px),
                        0 calc(${t * 100}% + ${t * 20}px)
                    );
                `;
            },
        };
    }
</script>

<div class="relative w-full">
    <div class="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-(--accent) to-transparent opacity-67"></div>

    <button type="button" class="w-full flex items-center justify-between py-5 md:py-6 text-left focus:outline-none group cursor-pointer bg-transparent border-none" onclick={() => (isOpen = !isOpen)} aria-expanded={isOpen}>
        <div class="flex items-center gap-4 md:gap-5">
            <span class="font-mono text-2xl md:text-3xl text-(--accent) transition-transform duration-300 {isOpen ? 'rotate-90' : ''}"> &gt; </span>
            <h3 class="font-heading text-xl md:text-2xl text-(--text) group-hover:text-(--accent) transition-colors duration-300 pr-4">
                {question}
            </h3>
        </div>
    </button>

    {#if isOpen}
        <div class="pb-6 font-content text-sm md:text-base text-(--text-h) leading-relaxed" transition:angledSlide={{ duration: 400 }}>
            {@render children()}
        </div>
    {/if}
</div>
