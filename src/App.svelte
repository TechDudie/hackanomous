<script>
    import { Mouse } from "lucide-svelte";
    import hackclub from "./assets/hackclub.svg";
    import orpheus from "./assets/orpheus.svg";
    import mascotDark from "./assets/mascot_dark.svg";

    import { gsap } from "gsap";

    import { ScrollTrigger } from "gsap/ScrollTrigger";
    import { ScrollSmoother } from "gsap/ScrollSmoother";

    gsap.registerPlugin(ScrollTrigger,ScrollSmoother);

    const smoothie = ScrollSmoother.create({
        smooth: 1,
        effects: true,
        normalizeScroll: true
    });
</script>

<div id="smooth-wrapper">
    <div id="smooth-content">
        <!-- hackclub icon -->
        <section class="absolute top-[1.5rem] left-1/2 -translate-x-1/2 z-50 flex items-center gap-2">
            <h6 class="text-(--accent-border) ml-[25.3px]">a hack</h6>
            <a href="https://hackclub.com" target="_blank" rel="noopener noreferrer" class="block">
                <img src={hackclub} class="cursor-pointer transition-all duration-300 ease-out hover:-translate-y-1 hover:scale-105 hover:drop-shadow-xl active:scale-95 active:-translate-y-1 active:duration-150" width="40" alt="Hack Club logo" />
            </a>
            <h6 class="text-(--accent-border)">club ysws</h6>
        </section>

        <!-- orpheus flag -->
        <section class="absolute top-0 left-[24px]">
            <a href="https://hackclub.com" target="_blank" rel="noopener noreferrer" class="block">
                <img src={orpheus} class="cursor-pointer" width="180" alt="Orpheus flag" />
            </a>
        </section>

        <!-- hackanomous presents -->
        <!-- not sure about this part, someone who has actual graphic design experience needs to figma it -->
        <!-- <section class="absolute top-[50dvh] left-1/2 translate-x-[-23rem] translate-y-[-12rem] -rotate-[15deg] z-1 underline underline-offset-2 decoration-(--accent-border)">
            <h6 class="font-mono text-(--accent-border) tracking-wider">hackanomous presents</h6>
        </section> -->
        
        <!-- landing -->
        <section class="min-h-[100dvh] flex justify-center items-center py-12 px-4 bg-[linear-gradient(150deg,#080E12,#0B1618)]">
            <div class="relative">
                <img src={mascotDark} class="base absolute top-3 -right-6" width="160" alt="anomaly, our mascot!" />
                <div class="w-fit border-2 border-dashed border-(--code-bg) rounded-2xl px-16 py-2 relative z-10 bg-[linear-gradient(175deg,var(--bg)_0%,#0B1618_33%,#080E12_100%)]">
                    <h3 class="font-content font-extralight text-sm text-(--text-h) tracking-widest">COMING SOON</h3>
                </div>
                <h1 class="font-heading font-regular text-7xl text-(--accent) mt-6">
                    BUILD <span class="font-semibold">AI</span>.
                </h1>
                <h1 class="font-heading font-regular text-7xl text-(--text) mt-4">
                    GET <span class="font-semibold">PRIZES</span>!
                </h1>
                <div class="mt-8 flex">
                    <input id="rsvp-input" class="flex-1 px-4 font-content font-light border-2 border-solid border-(--accent) text-(--accent-border) rounded-xl py-3 mr-4 focus:outline-none focus:border-(--accent-hover) focus:shadow-[0_0_67px_color-mix(in_srgb,var(--accent-hover)_6.7%,transparent)]" style="transition: box-shadow 0.35s ease-out, border-color 0.15s ease-out, background-color 0.15s ease-out;" type="text" placeholder="you@example.com" />
                    <button onclick={() => window.open("https://hackanomous-rsvp.fillout.com/t/4oPTMjqFuaus", "_blank")} class="font-content font-semibold border-2 border-solid border-(--accent) bg-(--accent) text-(--bg) rounded-xl px-10 py-3 cursor-pointer hover:bg-(--accent-hover) hover:border-(--accent-hover) hover:shadow-[0_0_67px_color-mix(in_srgb,var(--accent-hover)_6.7%,transparent)]" style="transition: box-shadow 0.35s ease-out, border-color 0.15s ease-out, background-color 0.15s ease-out;">RSVP!</button>
                </div>
            </div>
        </section>
        
        <!-- scroll down -->
        <section class="absolute top-[calc(100dvh-2rem)] left-1/2 -translate-x-1/2 -translate-y-full text-(--accent-border)">
            <div class="flex flex-row items-center gap-3 floater">
                <Mouse size={24} />
                <span class="font-content font-light text-base tracking-widest">SCROLL DOWN</span>
            </div>
        </section>
        
        <!-- NEXT VIEWPORT -->
        
        <section class="min-h-[100dvh] bg-[#000000] flex flex-col justify-center items-center py-20 px-4 sm:px-8 relative overflow-hidden">
            <!-- Subtle top border glow -->
            <div class="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-(--accent) to-transparent opacity-67"></div>
        
            <div class="max-w-5xl w-full flex flex-col lg:flex-row gap-16 items-center z-10">
                <div class="flex-1 space-y-8">
                    <h2 class="font-mono font-medium text-5xl md:text-7xl text-(--text)">
                        <span class="italic">DE</span>SLOP THE <br><span class="font-mono font-bold inline-block bg-clip-text text-transparent" style="background-image: linear-gradient(90deg, var(--accent) 0%, color-mix(in srgb, var(--accent) 90%, transparent) 100%);">WORLD</span>.
                    </h2>
                    <p class="font-mono font-normal text-lg md:text-xl leading-relaxed text-(--text-h)">the AI bubble might just be about to pop.<br><span class="font-bold text-(--text-l)">YOUR MISSION:</span> build projects incorporating AI that solve <u><span class="font-bold text-(--text-l)">real-world</span></u> problems.</p>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-4">
                        <div class="border-2 border-dashed border-(--code-bg) p-8 rounded-3xl bg-(--bg) hover:border-(--accent) transition-colors duration-300 group cursor-default">
                            <h4 class="font-heading text-4xl text-(--accent) mb-3 group-hover:scale-105 transition-transform origin-left drop-shadow-md">software</h4>
                            <p class="font-content text-base font-light text-(--text-h)">Build software that implements AI or Machine Learning to earn Bolts! Use them to buy including Raspberry PIs, AI Credits, RAM & GPU Grants, and more!</p>
                        </div>
                        <div class="border-2 border-dashed border-(--code-bg) p-8 rounded-3xl bg-(--bg) hover:border-(--accent) transition-colors duration-300 group cursor-default">
                            <h4 class="font-heading text-4xl text-(--accent) mb-3 group-hover:scale-105 transition-transform origin-left drop-shadow-md">hardware</h4>
                            <p class="font-content text-base font-light text-(--text-h)">Design hardware that implements AI or Machine Learning to receive funding to build it! Earn bolts for your physical work!</p>
                        </div>
                    </div>
        
                    <div class="pt-8">
                        <button onclick={() => window.scrollTo({ top: 0, behavior: "smooth" })} class="font-mono font-semibold border-2 border-solid border-(--accent) text-(--accent) hover:bg-(--accent) hover:text-(--bg) rounded-xl px-12 py-4 cursor-pointer focus:outline-none hover:-translate-y-1 hover:shadow-[0_0_30px_color-mix(in_srgb,var(--accent)_30%,transparent)] transition-all duration-300 tracking-wide text-lg"> REGISTER NOW </button>
                    </div>
                </div>
            </div>
        </section>
    </div>
</div>

<style>
    .floater {
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%,
        100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(12px);
        }
    }
</style>