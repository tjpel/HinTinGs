// {"question":"What is a webpage made of?","answer":"A webpage is made up of HTML, CSS, Javascript, and any other supporting files.","sources":" quants/Notion_DB/Building_Blocks_of_a_Webpage_b2fca7bc3f874cdeb889f45c1f4bad03.md"}

function contentHighlight(content: string, extract: string) {
	const lineCSSClass = 'mb-3';
	const finalJSX = [];
	const contentWithoutNewlines = content.replaceAll('\n', '');
	const extractWithoutNewlines = extract.replaceAll('\n', '').trim()
	let extractStart = contentWithoutNewlines.indexOf(extractWithoutNewlines);
	let extractEnd = -1;
	let hasExtract = false;
	if (extractStart > -1) {
		extractEnd = extractStart + extractWithoutNewlines.length - 1;
		hasExtract = true;
	}
	console.log(hasExtract);
	const contentLines = content.split('\n');
	let currentIndex = 0;
	for (let i = 0; i < contentLines.length; i++) {
		const line = contentLines[i];
		const lineEndIndex = currentIndex + line.length;
		// simple if extract not found
		if (extractStart === -1) {
			finalJSX.push(
				<p className={lineCSSClass} key={i}>
					{line}
				</p>
			);
			currentIndex = lineEndIndex;
			continue;
		}

		if (extractStart > currentIndex && extractEnd < lineEndIndex) {
			// extract within the line
			finalJSX.push(
				<p className={lineCSSClass} key={i}>
					{line.substring(0, extractStart - currentIndex)}
					<mark>
						{line.substring(extractStart - currentIndex, extractEnd - currentIndex)}
					</mark>
					{line.substring(extractEnd - currentIndex)}
				</p>
			);
			currentIndex = lineEndIndex;
			// set next found extract in content
			extractStart = contentWithoutNewlines.indexOf(extractWithoutNewlines, currentIndex);
			if (extractStart > -1) {
				extractEnd = extractStart + extract.trim().length - 1;
			}
		} else if (extractStart > currentIndex && extractStart < lineEndIndex) {
			// highlight starts within the line. 
			finalJSX.push(
				<p className={lineCSSClass} key={i}>
					{line.substring(0, extractStart - currentIndex)}
					<mark>
						{line.substring(extractStart - currentIndex)}
					</mark>
				</p>
			);
			currentIndex = lineEndIndex;
		} else if (extractEnd < lineEndIndex && extractEnd > currentIndex) {
			// highlight ends within the line
			finalJSX.push(
				<p className={lineCSSClass} key={i}>
					<mark>
						{line.substring(0, extractEnd - currentIndex)}
					</mark>
					{line.substring(extractEnd - currentIndex)}
				</p>
			);
			currentIndex = lineEndIndex;
			// set next found extract in content
			extractStart = contentWithoutNewlines.indexOf(extractWithoutNewlines, currentIndex);
			if (extractStart > -1) {
				extractEnd = extractStart + extract.trim().length - 1;
			}
		} else if (currentIndex >= extractStart && lineEndIndex <= extractEnd) {
			// entire line is part of extract
			finalJSX.push(
				<p className={lineCSSClass} key={i}>
					<mark>
						{line}
					</mark>
				</p>
			);
			currentIndex = lineEndIndex;
			if (lineEndIndex === extractEnd) {
				// set next found extract in content
				extractStart = contentWithoutNewlines.indexOf(extractWithoutNewlines, currentIndex);
				if (extractStart > -1) {
					extractEnd = extractStart + extract.trim().length - 1;
				}
			}
		} else {
			// line is not part of extract
			finalJSX.push(
				<p className={lineCSSClass} key={i}>
					{line}
				</p>
			);
			currentIndex = lineEndIndex;
		}
	}
	return {
		jsx: finalJSX,
		hasExtract: hasExtract
	};
}

export default contentHighlight;
