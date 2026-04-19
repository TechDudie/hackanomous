<script>
    import { onMount } from "svelte";
    
    import { gsap } from "gsap";
    import { ScrollSmoother } from "gsap/ScrollSmoother";
    import { ScrollTrigger } from "gsap/ScrollTrigger";
    import { Mouse } from "lucide-svelte";
    import p5 from "p5";

    import hackclub from "./assets/hackclub.svg";
    import mascotDark from "./assets/mascot_dark.svg";
    import orpheus from "./assets/orpheus.svg";
    import Question from "./lib/Question.svelte";

    /** @type {HTMLElement | undefined} */
    let overlay;

    onMount(() => {
        gsap.registerPlugin(ScrollTrigger, ScrollSmoother);
        const smoothie = ScrollSmoother.create({
            smooth: 1,
            effects: true,
            normalizeScroll: true
        });

        const renderer = new p5((p) => {
            /** @typedef {{ x: number; y: number; vx: number; vy: number }} CloudPoint */
            const LINK_DISTANCE = 143.11;
            /** @type {CloudPoint[]} */
            const points = [];

            const getPointCount = () => Math.max(67, Math.round((p.width * p.height * 128) / (1920 * 1080)));

            const randomVelocity = () => {
                const speed = p.random(0.10, 0.30);
                return speed * (p.random() > 0.5 ? 1 : -1);
            };

            const resetPoints = () => {
                points.length = 0;
                for (let i = 0; i < getPointCount(); i++) {
                    points.push({
                        x: p.random(p.width),
                        y: p.random(p.height),
                        vx: randomVelocity(),
                        vy: randomVelocity()
                    });
                }
            };

            p.setup = () => {
                if (!overlay) return;
                const canvas = p.createCanvas(window.innerWidth, window.innerHeight);
                canvas.parent(overlay);
                canvas.style("pointer-events", "none");
                p.pixelDensity(1);
                p.frameRate(60);
                resetPoints();
            };

            p.draw = () => {
                p.clear();

                for (let i = 0; i < points.length; i++) {
                    const point = points[i];
                    point.x += point.vx;
                    point.y += point.vy;

                    if (point.x <= 0 || point.x >= p.width) point.vx *= -1;
                    if (point.y <= 0 || point.y >= p.height) point.vy *= -1;
                }

                const maxDistanceSq = LINK_DISTANCE * LINK_DISTANCE;
                for (let i = 0; i < points.length; i++) {
                    for (let j = i + 1; j < points.length; j++) {
                        const dx = points[i].x - points[j].x;
                        const dy = points[i].y - points[j].y;
                        const d2 = dx * dx + dy * dy;
                        if (d2 > maxDistanceSq) continue;

                        const alpha = (1 - d2 / maxDistanceSq) * 67;
                        p.stroke(110, 255, 210, alpha);
                        p.strokeWeight(1);
                        p.line(points[i].x, points[i].y, points[j].x, points[j].y);
                    }
                }

                p.noStroke();
                p.fill(110, 255, 210, 115);
                for (let i = 0; i < points.length; i++) {
                    p.circle(points[i].x, points[i].y, 3.2);
                }
            };

            p.windowResized = () => {
                p.resizeCanvas(window.innerWidth, window.innerHeight);
                resetPoints();
            };
        });

        return () => {
            smoothie.kill();
            renderer.remove();
        };
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
        <section class="absolute top-[50dvh] left-1/2 translate-x-[-23rem] translate-y-[-11rem] -rotate-[15deg] z-1 underline underline-offset-2 decoration-(--accent-border) z-20">
            <h6 class="font-mono text-(--accent-border) tracking-wider">hackanomous presents</h6>
        </section>

        <section bind:this={overlay} class="absolute top-0 left-0 w-full h-full pointer-events-none z-0"></section>
        
        <!-- landing -->
        <section class="min-h-[100dvh] flex justify-center items-center py-12 px-4 bg-[linear-gradient(150deg,#080E12,#0B1618)]">
            <div class="relative">
                <img src={mascotDark} class="base absolute top-3 -right-6" width="160" alt="anomaly, our mascot!" />
                <div class="w-fit border-2 border-dashed border-(--code-bg) rounded-2xl px-16 py-2 relative z-10 bg-[linear-gradient(175deg,var(--bg)_0%,#0B1618_33%,#080E12_100%)]">
                    <h3 class="font-mono font-extralight text-sm text-(--text-h) tracking-widest">COMING SOON</h3>
                </div>
                <h1 class="font-heading font-regular text-7xl text-(--accent) mt-6">
                    BUILD <span class="font-semibold">AI</span>.
                </h1>
                <h1 class="font-heading font-regular text-7xl text-(--text) mt-4">
                    GET <span class="font-semibold">PRIZES</span>!
                </h1>
                <div class="mt-8 flex">
                    <input id="rsvp-input" class="flex-1 px-4 font-mono font-light border-2 border-solid border-(--accent) text-(--accent-border) rounded-xl py-3 mr-4 focus:outline-none focus:border-(--accent-hover) focus:shadow-[0_0_67px_color-mix(in_srgb,var(--accent-hover)_6.7%,transparent)]" style="transition: box-shadow 0.35s ease-out, border-color 0.15s ease-out, background-color 0.15s ease-out;" type="text" placeholder="you@example.com" />
                    <button onclick={() => window.open("https://hackanomous-rsvp.fillout.com/t/4oPTMjqFuaus", "_blank")} class="font-mono font-semibold border-2 border-solid border-(--accent) bg-(--accent) text-(--bg) rounded-xl px-10 py-3 cursor-pointer hover:bg-transparent hover:text-(--accent) hover:shadow-[0_0_67px_color-mix(in_srgb,var(--accent-hover)_6.7%,transparent)]" style="transition: box-shadow 0.35s ease-out, border-color 0.15s ease-out, background-color 0.15s ease-out, color 0.15s ease-out;">RSVP!</button>
                </div>
                <h6 class="font-mono font-light text-xs text-center text-(--text-h) tracking-widest mt-6">
                    ages 13-18 only. <span class="underline underline-offset-2">june 1</span> to <span class="underline underline-offset-2">sept 1</span>.
                </h6>
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
        <!-- disabled for now as i try to make first viewport less vibecoded -->
        {#if false}
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
        {/if}

        <section class="min-h-[100dvh] bg-[#000000] flex flex-col justify-center items-center py-20 px-4 sm:px-8 relative overflow-hidden">
            <div class="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-(--accent) to-transparent opacity-67"></div>

            <h1 class="font-mono font-base text-lg md:text-xl text-(--text) tracking-wider text-center">
                more info coming soon...
            </h1>

            <div class="absolute bottom-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-(--accent) to-transparent opacity-67"></div>
        </section>

        <!-- standard FAQ and closing info -->
        <section class="min-h-[100dvh] bg-[linear-gradient(150deg,#080E12,#0B1618)] px-6 md:px-12 xl:px-24 py-24 flex flex-col justify-start items-center">
            <div class="max-w-7xl mx-auto w-full">
                <h1 class="font-heading font-regular text-5xl md:text-6xl text-(--text) mb-12 w-full">FAQ</h1>

                <!-- TODO: answer more flipping questions -->
                <!-- TODO: also make actually look nice -->

                <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 lg:gap-x-24 gap-y-0 w-full">
                    <!-- column 1 -->
                    <div class="flex flex-col">
                        <Question question="Who can participate?">
                            <!-- vetted answer -->
                            <p>Anyone between the ages of 13 and 18 can participate in Hackanomous! We welcome students from all skill levels to join us in building and shipping the next generation of AI.</p>
                        </Question>
                        <Question question="What kind of projects can I build?">
                            <!-- vetted answer -->
                            <p>You can build any project incorporating AI or ML! Whether it's a software application, a hardware device, or something completely original and unique, we want to see your innovation shine.</p>
                        </Question>
                    </div>

                    <!-- column 2 -->
                    <div class="flex flex-col">
                        <Question question="What is the registration process?">
                            <!-- vetted answer -->
                            <p>Registration for Hackanomous is simple! Just scroll up and click the "RSVP" button to fill out the registration form.</p>
                        </Question>
                        <Question question="What are the prizes?">
                            <!-- vetted answer -->
                            <p>We have a variety of exciting prizes for our participants! Shipped projects will receive Bolts, which can be redeemed for Raspberry Pis, AI Credits, RAM & GPU Grants, and more.</p>
                        </Question>
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