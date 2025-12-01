<script lang="ts">
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import { ToggleGroup, RadioButton } from 's-comp-core';
	import type { ChartOptions } from '../components/chartTypes';
	import BarChart from '../components/BarChart.svelte';
	import LineChart from '../components/LineChart.svelte';

	// NOTE: Tab 컴포넌트에 해당 컴포넌트가 설정된 탭이 선택될 경우에
	//       컴포넌트 내부에 'update' 함수 존재 여부를 동적으로 확인해서 호출해준다.
	export function update() {
		chartOptions = { ...chartOptions }; // 차트를 다시 그리게 한다.
	}

	// 차트 크기 관련 변수들
	const chartWidth = 800;
	const chartHeight = 400;
	const margin = { top: 20, right: 30, bottom: 40, left: 40 };

	let frequencyData: any = null;
	let frequencyWithBonus = true;
	let totalDraws = 0;

	let chartOptions: ChartOptions = {
		type: 'bar_chart',
		data: [],
		width: chartWidth,
		height: chartHeight,
		margin: margin,
		barColorDefault: 'steelblue',
		barColorHover: 'orange',
		barColorSameValue: '#FFD580',
		stripeColor: 'rgba(255, 140, 0, 0.4)',
		highlightColorMin: '#FF5722',
		highlightColorMax: '#9575CD',
		highlightColorMid: '#8BC34A',
		textColorFrequency: '#FF6B6B',
		guideLineColor: '#00BCD4',
		transitionDuration: 100,
		barBorderColor: '#FF8C00'
	};

	// 빈도 데이터를 업데이트하고 총 회차를 계산하는 함수
	function updateFrequencyData(data: any) {
		const frequencyWithoutBonus = [...data.cumulative_stats.frequency_without_bonus];
		const frequencyWithBonus = [...data.cumulative_stats.frequency_with_bonus];

		// recent_draws의 데이터를 반영
		const recentDrawNumbers = Object.keys(data.recent_draws).map((key) =>
			parseInt(key.replace('draw_', ''))
		);
		const maxRecentDraw = Math.max(...recentDrawNumbers);

		Object.values(data.recent_draws).forEach((draw: any) => {
			draw.winning_numbers.forEach((num: number) => {
				frequencyWithoutBonus[num - 1]++;
				frequencyWithBonus[num - 1]++;
			});
			frequencyWithBonus[draw.bonus_number - 1]++;
		});

		return {
			frequency_without_bonus: frequencyWithoutBonus,
			frequency_with_bonus: frequencyWithBonus,
			totalDraws: maxRecentDraw
		};
	}

	let frequencyDataWithBonus: number[] = [];
	let frequencyDataWithoutBonus: number[] = [];

	onMount(async () => {
		const response = await fetch(`${base}/data/frequency.json`);
		const rawData = await response.json();

		// 빈도 데이터 업데이트 및 총 회차 계산
		const {
			frequency_without_bonus,
			frequency_with_bonus,
			totalDraws: updatedTotalDraws
		} = updateFrequencyData(rawData);

		frequencyDataWithBonus = frequency_with_bonus;
		frequencyDataWithoutBonus = frequency_without_bonus;

		frequencyData = {
			...rawData,
			cumulative_stats: {
				...rawData.cumulative_stats,
				frequency_without_bonus,
				frequency_with_bonus,
				end_draw: updatedTotalDraws // end_draw 업데이트
				}
			};

		// totalDraws 설정
		totalDraws = updatedTotalDraws;
	});

	$: if (frequencyData) {
		if (chartOptions.type === 'line_chart') {
			chartOptions = {
				...chartOptions,
				dataWithoutBonus: frequencyDataWithoutBonus,
				dataWithBonus: frequencyDataWithBonus
			};
		} else {
			chartOptions = {
				...chartOptions,
				data: frequencyWithBonus ? frequencyDataWithBonus : frequencyDataWithoutBonus
			};
		}
	}

	function handleToggleItemChanged(event: CustomEvent) {
		if (event.detail.value === 'line_chart') {
			chartOptions = { ...chartOptions, type: 'line_chart' };
			frequencyWithBonus = false;
		} else {
			chartOptions = { ...chartOptions, type: 'bar_chart' };
			frequencyWithBonus = event.detail.value === 'frequency_with_bonus';
		}
	}
</script>

<div class="lotto-frequency">
	<h2>총 {totalDraws}회</h2>
	<ToggleGroup
		direction="vertical"
		hAlign="right"
		items={[
			{ component: RadioButton, label: '꺽은선 그래프', value: 'line_chart' },
			{ component: RadioButton, label: '보너스 번호 포함', value: 'frequency_with_bonus' },
			{ component: RadioButton, label: '보너스 번호 제외', value: 'frequency_without_bonus' }
		]}
		activatedValue="frequency_with_bonus"
		on:toggleItemChanged={handleToggleItemChanged}
	/>
	{#if frequencyData}
		{#if chartOptions.type === 'bar_chart'}
			<div class="stats">
				<BarChart {chartOptions} maxWidth="800px" />
			</div>
		{:else if chartOptions.type === 'line_chart'}
			<LineChart 
				{chartOptions} 
				maxWidth="900px"
				legendPadding={{ top: 0, right: 0, bottom: 0, left: 10 }}
				colorWithBonus="orange"
				colorWithoutBonus="steelblue"
				verticalLineColor="#FF4081"
			/>
		{:else}
			<p>차트 타입이 올바르지 않습니다.</p>
		{/if}
	{:else}
		<p>로딩 중...</p>
	{/if}
</div>

<style lang="scss">
	.lotto-frequency {
		padding: 0 1em 0.5em 1em;
		font-family: 'Noto Sans KR', sans-serif;

		h2 {
			text-align: center;
			margin-bottom: 1em;
		}

		.stats {
			display: flex;
			justify-content: center;
			margin: 1em;
		}
	}
</style>
