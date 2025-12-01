<script lang="ts">
	export let number: number;

	function getColor(n: number): string {
		if (n <= 10) return '#fbc400'; // Yellow
		if (n <= 20) return '#69c8f2'; // Blue
		if (n <= 30) return '#ff7272'; // Red
		if (n <= 40) return '#a1a1a1'; // Gray (Black is too dark for text usually, but standard is Gray/Black)
		return '#b0d840'; // Green
	}

	$: color = getColor(number);
</script>

<div class="ball" style="background-color: {color};">
	<span class="number">{number}</span>
</div>

<style>
	.ball {
		display: inline-flex;
		justify-content: center;
		align-items: center;
		width: 2.5em;
		height: 2.5em;
		border-radius: 50%;
		margin: 0.2em;
		box-shadow: inset -2px -2px 6px rgba(0, 0, 0, 0.2), 2px 2px 4px rgba(0, 0, 0, 0.1);
		color: white;
		font-weight: bold;
		font-family: 'Helvetica Neue', Arial, sans-serif;
		text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
		border: 1px solid rgba(0, 0, 0, 0.05);
	}

	.number {
		font-size: 1.2em;
	}
</style>
