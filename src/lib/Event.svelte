<script>
	export let left = "0dvw";
	export let placement = "top";
	export let date = "";
	export let title = "";
	export let description = "";
	export let href = "";

	$: isTop = placement === "top";
	$: stemClass = isTop
		? "absolute bottom-0 left-0 w-[2px] h-[120px] bg-(--accent) origin-bottom rotate-[30deg]"
		: "absolute top-0 left-0 w-[2px] h-[120px] bg-(--accent) origin-top rotate-[-30deg]";
	$: cardClass = isTop
		? "absolute bottom-[104px] left-[60px] w-[260px] border-b-2 border-(--accent) pb-4"
		: "absolute top-[104px] left-[60px] w-[260px] border-t-2 border-(--accent) pt-4";
</script>

<div class="absolute top-1/2 group" style={`left: ${left};`}>
	<div class={stemClass}></div>
	<div class={cardClass}>
		<h4 class="font-mono text-2xl text-(--accent) font-semibold tracking-widest uppercase">{date}</h4>
		<h5 class="font-heading text-xl text-(--text) mt-3 leading-tight tracking-wide">{title}</h5>

		{#if href}
			<p class="font-content text-(--text-h) text-sm mt-2 opacity-80">
				<a href={href} target="_blank" rel="noopener noreferrer" class="underline">{description}</a>
			</p>
		{:else}
			<p class="font-content text-(--text-h) text-sm mt-2 opacity-80">{description}</p>
		{/if}
	</div>
</div>
