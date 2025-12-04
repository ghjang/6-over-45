<script lang="ts">
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import { Tab } from 's-comp-core';
	import LottoFrequency from './LottoFrequency.svelte';
	import NextGuess from './NextGuess.svelte';
	import PreviousDrawResult from './PreviousDrawResult.svelte';

	let tab: Tab;

	let tabs = [
		{
			label: '로또 당첨 번호 빈도',
			component: LottoFrequency,
			componentClassName: undefined
		},
		{
			label: '직전 회차 당첨 결과', // Initial placeholder
			component: PreviousDrawResult,
			componentClassName: undefined
		},
		{
			label: '다음 당첨 번호 뽑기',
			component: NextGuess,
			componentClassName: undefined
		}
	];

	onMount(async () => {
		try {
			const response = await fetch(`${base}/data/latest_lottery_result.json`);
			const data = await response.json();
			const currentDrawNumber = parseInt(data.draw_number);
			const nextDrawNumber = currentDrawNumber + 1;

			tabs = [
				tabs[0],
				{
					...tabs[1],
					label: `${currentDrawNumber}회 당첨 결과`
				},
				{
					...tabs[2],
					label: `${nextDrawNumber}회 당첨 번호 뽑기`
				}
			];
		} catch (e) {
			console.error('Failed to fetch lottery data:', e);
		}
	});
</script>

<div class="tab-container">
	<Tab bind:this={tab} selectedTabIndex={2} {tabs} />
</div>

<style lang="scss">
	.tab-container {
		border: 1px solid darkgray;
		border-radius: 1px;
	}
</style>
