<script lang="ts">
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	import type { ChartOptions } from './chartTypes';

	export let chartOptions: ChartOptions;
	export let maxWidth: string = '800px';
	export let legendPadding: { top: number; right: number; bottom: number; left: number } = {
		top: 0,
		right: 5,
		bottom: 5,
		left: 5
	};
	export let colorWithBonus: string = 'orange';
	export let colorWithoutBonus: string = 'steelblue';
	export let verticalLineColor: string = '#FF4081';  // 새로운 prop: 동적 점선 색상

	let svg: SVGSVGElement;
	let chart: d3.Selection<SVGGElement, unknown, null, undefined>;
	let crosshairGroup: d3.Selection<SVGGElement, unknown, null, undefined>;

	$: if (svg && chartOptions) {
		drawLineChart(svg, chartOptions);
	}

	function drawLineChart(svg: SVGSVGElement, options: ChartOptions) {
		const { width, height, margin, dataWithoutBonus, dataWithBonus } = options;
		const legendWidth = 120; // 범례의 너비 설정
		const chartWidth = width - margin.left - margin.right - legendWidth; // 차트 너비에서 범례 너비 빼기
		const chartHeight = height - margin.top - margin.bottom;

		d3.select(svg)
			.selectAll('*')
			.remove();

		chart = d3.select(svg)
			.attr('width', width)
			.attr('height', height)
			.append('g')
			.attr('transform', `translate(${margin.left},${margin.top})`);

		crosshairGroup = chart.append('g').attr('class', 'crosshair-group');

		const x = d3.scaleLinear().domain([1, 45]).range([0, chartWidth]);

		// Y축 도메인 조정
		const yMax = Math.max(d3.max(dataWithoutBonus || []) || 0, d3.max(dataWithBonus || []) || 0);
		const y = d3
			.scaleLinear()
			.domain([0, yMax * 1.1]) // 최대값에서 10% 여유를 둡니다.
			.range([chartHeight, 0]);

		// X축 그리드 라인 추가
		chart
				.append('g')
				.attr('class', 'grid')
				.attr('opacity', 0.1)
				.call(
					d3
						.axisBottom(x)
						.tickSize(chartHeight)
						.tickFormat(null as any)
				);

		// Y축 그리드 라인 추가
		chart
			.append('g')
			.attr('class', 'grid')
			.attr('opacity', 0.1)
			.call(
				d3
					.axisLeft(y)
					.tickSize(-chartWidth)
					.tickFormat(null as any)
			);

		// X축
		chart
			.append('g')
			.attr('transform', `translate(0,${chartHeight})`)
			.call(d3.axisBottom(x).ticks(10));

		// Y축
		chart.append('g').call(d3.axisLeft(y));

		// 라인 그리기 (데이터 포인트 이전에)
		function drawLine(data: number[], color: string) {
			const line = d3.line<number>()
				.x((d, i) => x(i + 1))
				.y(d => y(d))
				.curve(d3.curveMonotoneX);

			chart.append('path')
				.datum(data)
				.attr('fill', 'none')
				.attr('stroke', color)
				.attr('stroke-width', 2)
				.attr('d', line);
		}

		if (dataWithoutBonus) drawLine(dataWithoutBonus, colorWithoutBonus);
		if (dataWithBonus) drawLine(dataWithBonus, colorWithBonus);

		// 데이터 포인트 추가 및 이벤트 핸들러 설정
		function addDataPoints(data: number[], className: string, color: string) {
			return chart.selectAll(`.${className}`)
				.data(data)
				.join('circle')
				.attr('class', className)
				.attr('cx', (d, i) => x(i + 1))
				.attr('cy', d => y(d))
				.attr('r', 3.5)
				.attr('fill', color);
		}

		let dotsWithoutBonus, dotsWithBonus;
		if (dataWithoutBonus) {
			dotsWithoutBonus = addDataPoints(dataWithoutBonus, 'dot-without-bonus', colorWithoutBonus);
		}
		if (dataWithBonus) {
			dotsWithBonus = addDataPoints(dataWithBonus, 'dot-with-bonus', colorWithBonus);
			}

		// 마우스 이벤트를 감지할 투명한 영역 추가
		const overlay = chart.append('rect')
			.attr('class', 'overlay')
			.attr('width', chartWidth)
			.attr('height', chartHeight)
			.style('fill', 'none')
			.style('pointer-events', 'all');

		overlay
			.on('mousemove', function(event) {
				const [xPos, yPos] = d3.pointer(event);
				const xValue = Math.round(x.invert(xPos));
				
				drawVerticalLine(xPos);
				drawHorizontalLines(xValue);
			})
			.on('mouseout', handleMouseOut);

		function handleMouseOut() {
			crosshairGroup.selectAll('.crosshair').remove();
			chart.selectAll('.highlight-point').remove();
		}

		function drawVerticalLine(xPos: number) {
			crosshairGroup.selectAll('.vertical-line').remove();
			
			crosshairGroup.append('line')
				.attr('class', 'crosshair vertical-line')
				.attr('x1', xPos)
				.attr('y1', 0)
				.attr('x2', xPos)
				.attr('y2', chartHeight)
				.attr('stroke', verticalLineColor)
				.attr('stroke-width', 1.5)
				.attr('stroke-dasharray', '5,3');
		}

		function drawHorizontalLines(xValue: number) {
			crosshairGroup.selectAll('.horizontal-line').remove();
			
			if (xValue >= 1 && xValue <= 45) {
				const index = xValue - 1;
				if (dataWithoutBonus && index < dataWithoutBonus.length) {
					drawHorizontalLine(y(dataWithoutBonus[index]));
				}
				if (dataWithBonus && index < dataWithBonus.length) {
					drawHorizontalLine(y(dataWithBonus[index]));
				}
			}
		}

		function drawHorizontalLine(yPos: number) {
			crosshairGroup.append('line')
				.attr('class', 'crosshair horizontal-line')
				.attr('x1', 0)
				.attr('y1', yPos)
				.attr('x2', chartWidth)
				.attr('y2', yPos)
				.attr('stroke', verticalLineColor)  // Y축 수직선과 동일한 색상 사용
				.attr('stroke-width', 1.5)
				.attr('stroke-dasharray', '5,3');
		}

		// 디버깅용: 데이터 포인트 개수 확인
		console.log('Number of dots without bonus:', dotsWithoutBonus ? dotsWithoutBonus.size() : 0);
		console.log('Number of dots with bonus:', dotsWithBonus ? dotsWithBonus.size() : 0);

		// 범례 추가
		const legend = chart.append('g')
			.attr('font-family', 'sans-serif')
			.attr('font-size', 10)
			.attr('text-anchor', 'start')
			.attr('transform', `translate(${chartWidth + 10},${legendPadding.top})`);

		const legendItems = legend.selectAll('g')
			.data(['보너스 번호 포함', '보너스 번호 제외'])
			.enter()
			.append('g')
			.attr('transform', (d, i) => `translate(0,${i * 20})`);

		legendItems.append('rect')
			.attr('x', 0)
			.attr('width', 19)
			.attr('height', 19)
			.attr('fill', (d, i) => i === 0 ? colorWithBonus : colorWithoutBonus);

		legendItems.append('text')
			.attr('x', 25)
			.attr('y', 9.5)
			.attr('dy', '0.32em')
			.text(d => d);
	}
</script>

<div class="chart-container" style:max-width={maxWidth}>
	<svg bind:this={svg}></svg>
</div>

<style lang="scss">
	.chart-container {
		width: 100%;
		overflow-x: auto;

		svg {
			display: block;
			margin: 0 auto;
		}
	}
</style>
