import { useEffect, useState } from "react";
import Overlay from "../components/overlay";
import { protectedFetch, API_URL } from '../utils/fetch';
import Loading from "../components/loading";
import { Source } from "./index";
import contentHighlight from "../utils/contentHighlight";

type Document = {
	name: string,
	content: string
};

type Props = {
	show: boolean,
	source?: Source,
	onClose: () => void
};

function SourceDocOverlay({ show, source, onClose }: Props) {
	const [fetchingDocument, setFetchingDocument] = useState(true);
	const [document, setDocument] = useState<Document>();

	useEffect(() => {
		if (!source?.name) {
			return;
		}
		const url = API_URL + '/documents/' + encodeURIComponent(source.name.trim().replaceAll('_', ' '));
		const options = {
			method: 'GET'
		};
		protectedFetch<Document>(url, options).then(res => {
			setDocument(res);
			setFetchingDocument(false);
		}).catch(err => {
			alert((err.message ? err.message : JSON.stringify(err)));
		});
	}, [source?.name]);

	let documentJSX: JSX.Element[] = [];
	let containsExtract = false;
	if (document && source) {
		const highlightedContent = contentHighlight(document.content, source.extract);
		documentJSX = highlightedContent.jsx;
		containsExtract = highlightedContent.hasExtract;
	}

	let mainContent;
	if (fetchingDocument || !document) {
		mainContent = (<>
			<h4 className="mb-3 text-xl text-center font-bold">Fetching Original Document</h4>
			<Loading />
			<p className="text-center mt-3">Thank you for your patience</p>
		</>);
	} else {
		mainContent = (<>
			<h1 className="text-2xl font-bold mb-5">
				{document.name}
			</h1>
			{
				!containsExtract ?
					<p className="text-sm mb-5 text-red-600 italic">
						Warning! We we weren't able to find the passage cited by the AI! Double check the answer for correctness!
					</p>
					:
					null
			}
			{documentJSX}
		</>);
	}

	return (
		<Overlay show={show} className='max-w-2xl mx-auto px-5'>
			<button 
				className="text-xl text-white hover:text-gray-300 w-full text-left mt-10 md:mt-20 pb-5"
				onClick={onClose}
			>
				Close X
			</button>
			<div className='bg-white py-10 px-5 sm:px-10 rounded-2xl max-h-[80vh] overflow-y-auto'>
				{mainContent}
			</div>
		</Overlay>
	);
}

export default SourceDocOverlay;
