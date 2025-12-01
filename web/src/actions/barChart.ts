import * as d3 from 'd3';

interface BarChartOptions {
	data: number[];
	width: number;
	height: number;
	margin: { top: number; right: number; bottom: number; left: number };
	barColorDefault: string;
	barColorHover: string;
	barColorSameValue: string;
	stripeColor: string;
	highlightColorMin: string;
	highlightColorMax: string;
	highlightColorMid: string;
	textColorFrequency: string;
	guideLineColor: string;
	transitionDuration: number;
	barBorderColor: string;
}

export function barChart(node: SVGElement, options: BarChartOptions) {
	let chart: d3.Selection<SVGGElement, unknown, null, undefined>;
	let bars: d3.Selection<SVGRectElement, number, SVGGElement, unknown>;
	let guideLine: d3.Selection<SVGLineElement, unknown, null, undefined>;

	function init() {
		const svg = d3
			.select(node)
			.attr('width', '100%')
			.attr('height', options.height)
			.attr('viewBox', `0 0 ${options.width} ${options.height}`)
			.attr('preserveAspectRatio', 'xMidYMid meet');

		chart = svg
			.append('g')
			.attr('transform', `translate(${options.margin.left},${options.margin.top})`);

		// 나머지 초기화 로직...

		// 가이드 라인 위한 그룹 추가
		const guideLineGroup = chart.append('g').attr('class', 'guide-line-group');

		// 가이드 라인 생성 (초기에는 숨김)
		guideLine = guideLineGroup
			.append('line')
			.attr('class', 'guide-line')
			.attr('x1', 0)
			.attr('x2', options.width)
			.attr('stroke', options.guideLineColor)
			.attr('stroke-width', 1)
			.attr('stroke-dasharray', '3,3')
			.attr('stroke-opacity', 0.7)
			.style('display', 'none');

		// SVG에 패턴 정의 추가
		const defs = d3.select(node).append('defs');

		defs
			.append('pattern')
			.attr('id', 'stripe-pattern')
			.attr('patternUnits', 'userSpaceOnUse')
			.attr('width', 8)
			.attr('height', 8)
			.attr('patternTransform', 'rotate(45)')
			.append('rect')
			.attr('width', 4)
			.attr('height', 8)
			.attr('transform', 'translate(0,0)')
			.attr('fill', options.stripeColor)
			.attr('fill-opacity', 0.4); // 빗금 패턴의 기본 불투명도 설정
	}

	function update(options: BarChartOptions) {
		// 기존 차트 요소들을 모두 제거
		chart.selectAll('*').remove();

		const width = options.width - options.margin.left - options.margin.right;
		const height = options.height - options.margin.top - options.margin.bottom;

		// x와 y 스케일 정의
		const x = d3
			.scaleBand()
			.range([0, width])
			.domain(options.data.map((d, i) => (i + 1).toString()))
			.padding(0.1);

		const y = d3
			.scaleLinear()
			.range([height, 0])
			.domain([0, d3.max(options.data) || 0]);

		// 축 추가
		chart
			.append('g')
			.attr('class', 'x-axis')
			.attr('transform', `translate(0,${height})`)
			.call(d3.axisBottom(x));
		chart.append('g').attr('class', 'y-axis').call(d3.axisLeft(y));

		// 최대값, 최소값, 중위수 찾기
		const maxValue = Math.max(...options.data);
		const minValue = Math.min(...options.data);
		const maxIndex = options.data.indexOf(maxValue);
		const minIndex = options.data.indexOf(minValue);
		const sortedData = [...options.data].sort((a, b) => a - b);
		const medianValue = sortedData[Math.floor(sortedData.length / 2)];
		const medianIndex = options.data.indexOf(medianValue);

		// 막대 그래프 그리기
		bars = chart
			.selectAll<SVGRectElement, number>('.bar')
			.data(options.data)
			.enter()
			.append('rect')
			.attr('class', 'bar')
			.attr('x', (d, i) => x((i + 1).toString()) as number)
			.attr('y', (d) => y(d))
			.attr('width', x.bandwidth())
			.attr('height', (d) => height - y(d))
			.attr('data-index', (d, i) => i)
			.attr('fill', (d, i) => {
				if (i === maxIndex) return options.highlightColorMax;
				if (i === minIndex) return options.highlightColorMin;
				if (i === medianIndex) return options.highlightColorMid;
				return options.barColorDefault;
			});

		// 빈도수 텍스트 추가
		chart
			.selectAll('.bar-label')
			.data(options.data)
			.enter()
			.append('text')
			.attr('class', 'bar-label')
			.attr('x', (d, i) => (x((i + 1).toString()) as number) + x.bandwidth() / 2)
			.attr('y', (d) => y(d) - 2)
			.attr('text-anchor', 'middle')
			.text((d) => d)
			.attr('fill', options.textColorFrequency)
			.attr('font-size', '0.5em')
			.attr('font-weight', 'bold');

		// 삼각형과 min/mid/max 레이블 추가 함수
		function addArrowsAndLabels() {
			const xAxisNode = chart.select('.x-axis').node() as SVGGElement;
			if (!xAxisNode) return;

			const xAxisBBox = xAxisNode.getBBox();
			const xAxisHeight = xAxisBBox.height;

			const arrowSize = 6;
			const arrowOffset = 5;
			const labelOffset = xAxisHeight + arrowSize + 15;

			function createArrowPath(x: number, y: number) {
				return `M${x},${y} L${x - arrowSize / 2},${y + (arrowSize * Math.sqrt(3)) / 2} L${x + arrowSize / 2},${y + (arrowSize * Math.sqrt(3)) / 2} Z`;
			}

			function addArrowAndLabel(index: number, label: string, color: string) {
				const xPosition = (x((index + 1).toString()) as number) + x.bandwidth() / 2;
				const yPosition = height + xAxisHeight + arrowOffset;

				chart.append('path').attr('d', createArrowPath(xPosition, yPosition)).attr('fill', color);

				chart
					.append('text')
					.attr('x', xPosition)
					.attr('y', height + labelOffset)
					.attr('text-anchor', 'middle')
					.attr('fill', color)
					.attr('font-weight', 'bold')
					.attr('font-size', '0.5em')
					.text(label);
			}

			addArrowAndLabel(minIndex, 'min', options.highlightColorMin);
			addArrowAndLabel(medianIndex, 'mid', options.highlightColorMid);
			addArrowAndLabel(maxIndex, 'max', options.highlightColorMax);
		}

		// NOTE: 정확한 위치 계산을 위해서 딜레이가 필요하다.
		requestAnimationFrame(() => addArrowsAndLabels());

		// 마우스 오버 효과 추가
		bars
			.on('mouseover', function (event, d) {
				const currentBar = d3.select(this);
				const currentIndex = parseInt(currentBar.attr('data-index') || '');

				currentBar
					.transition()
					.duration(options.transitionDuration)
					.attr('fill', options.barColorHover);

				bars
					.filter(function (data, index) {
						return data === d && index !== currentIndex;
					})
					.transition()
					.duration(options.transitionDuration)
					.attr('fill', options.barColorSameValue)
					.attr('stroke', options.barBorderColor)
					.attr('stroke-width', 1)
					.style('fill', `url(#stripe-pattern)`)
					.style(
						'transition',
						`fill ${options.transitionDuration}ms ${options.transitionDuration}ms, 
                         fill-opacity ${options.transitionDuration}ms ${options.transitionDuration * 2}ms`
					);

				guideLine.attr('y1', y(d)).attr('y2', y(d)).style('display', 'block');
			})
			.on('mouseout', function () {
				bars
					.transition()
					.duration(options.transitionDuration)
					.attr('fill', (d, i) => {
						if (i === maxIndex) return options.highlightColorMax;
						if (i === minIndex) return options.highlightColorMin;
						if (i === medianIndex) return options.highlightColorMid;
						return options.barColorDefault;
					})
					.style('fill', null)
					.style('transition', '')
					.attr('stroke', 'none')
					.attr('stroke-width', 0);

				guideLine.style('display', 'none');
			});

		// 가이드라인 재생성
		guideLine = chart
			.append('line')
			.attr('class', 'guide-line')
			.attr('x1', 0)
			.attr('x2', width)
			.attr('stroke', options.guideLineColor)
			.attr('stroke-width', 1)
			.attr('stroke-dasharray', '3,3')
			.attr('stroke-opacity', 0.7)
			.style('display', 'none');
	}

	init();
	update(options);

	return {
		update(newOptions: Partial<BarChartOptions>) {
			Object.assign(options, newOptions);
			update(options);
		},
		destroy() {
			d3.select(node).selectAll('*').remove();
		}
	};
}
