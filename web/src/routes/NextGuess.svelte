<script lang="ts">
	import { onMount } from 'svelte';
	import { base } from '$app/paths';

	import LottoBall from '../components/LottoBall.svelte';

	type NextGuessData = {
		next_guesses: number[][];
	};

	let nextGuessesData: NextGuessData = {
		next_guesses: [],
	};

	onMount(async () => {
		const response = await fetch(`${base}/data/next_guess.json`);
		nextGuessesData = await response.json();
	});
</script>

<div class="next-guess">
	{#if nextGuessesData.next_guesses.length > 0}
		<ul>
			{#each nextGuessesData.next_guesses as guess}
				<li>
					{#each guess as number}
						<LottoBall {number} />
					{/each}
				</li>
			{/each}
		</ul>
	{:else}
		<p>로딩 중...</p>
	{/if}
</div>

<style lang="scss">
	.next-guess {
		padding: 0.1em 0.5em;

		ul {
			list-style-type: none;
			padding: 0;
			li {
				width: max-content;
				background: #f4f4f4;
				margin: 0.5em 0;
				padding: 0.5em;
				border-radius: 8px;
				display: flex;
				gap: 0.2em;
			}
		}
	}
</style>
