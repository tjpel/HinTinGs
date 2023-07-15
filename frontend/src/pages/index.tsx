import { useRef, useState, useEffect } from 'react';
import Button from '../components/button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import s from '../styles/index.module.scss';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';
import Document from '../components/document';
import UploadIcon from '../assets/upload.svg';
import CiteIcon from '../assets/cite.svg';
import UploadOverlay from './upload';
import { API_URL, protectedFetch } from '../utils/fetch';
import Loading from '../components/loading';
import SourceDocOverlay from './source';

export type Source = {
	name: string,
	id: string,
	extract: string
};

type Answer = {
	question: string,
	answer: string,
	sources: Source[]
};

function IndexPage() {
	const [question, setQuestion] = useState('');
	const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
	const [answer, setAnswer] = useState<null | Answer>(null);
	const [processingAnswer, setProcessingAnswer] = useState(false);
	const [showUploadOverlay, setShowUploadOverlay] = useState(false);
	const [showSourceOverlay, setShowSourceOverlay] = useState(false);
	const [viewedSource, setViewedSource] = useState<Source>();

	// useEffect(() => {
	// 	const url = API_URL + '/documents/';
	// 	const options = {
	// 		method: 'GET'
	// 	};
	// 	protectedFetch<string[]>(url, options).then(res => {
	// 		setUploadedFiles(res);
	// 	}).catch(err => {
	// 		alert('failed to get uploaded documents!');
	// 	});
	// }, []);

	const handleSubmit = (e) => {
		e.preventDefault();
		//alert('submitting question')
		onQuestionAsked();
	}

	const onQuestionAsked = () => {
		//console.log("Asking question " + question)
		setProcessingAnswer(true);
		const url = API_URL + '/query/';
		const options = {
			method: 'POST',
			body: JSON.stringify({
				question
			}),
			headers: {
				'Content-Type': 'application/json'
			}
		};
		protectedFetch<Answer>(url, options).then(res => {
			//console.log("Receiving answer" + res);
			setAnswer(res);
			setProcessingAnswer(false);
			setQuestion('');
		}).catch(err => {
			console.log("Error receiving answer " + err);
			alert((err.message ? err.message : JSON.stringify(err)));
		});
	};

	const uploadedFilesJSX = uploadedFiles.map((file, i) => {
		let ext = file.name.split('.')[1];
		// if (file.type === 'plain/markdown') {
		// 	ext = 'md';
		// }
		return (
			<Document 
				key={i}
				className='shadow-md mb-3 text-white bg-green-500 hover:bg-green-600' 
				name={file.name}
				ext={ext}
			/>
		);
	});

	let sourcesJSX;
	if (answer) {
		const sourceArray = answer.sources;
		sourcesJSX = sourceArray.map((src, i) => (
			<li 
				className='mb-3' key={i}
				onClick={() => {
					setViewedSource(src);
					setShowSourceOverlay(true);
				}}
			>
				<img className='inline-block w-5 h-5 mr-3' src={CiteIcon} alt="Cite source" />
				<button className='hover:text-gray-500'>{src.name}</button>
			</li>
		));
	}

	let mainContent;

	if (uploadedFiles.length === 0) {
		mainContent = (<>
			<h1 className='text-4xl text-center mb-10'>
				<img className='inline-block w-14 h-14' src='/hintings_logo_green.png' alt='hintings logo' />{' '}
				HiNTinGs
			</h1>
			<Button 
				className='px-5 py-2 rounded-full text-white mx-auto block' bg='green'
				onClick={() => setShowUploadOverlay(true)}
			>
				upload a document to get started{' '}
				<img className='inline-block w-5 h-5' src={UploadIcon} alt="Upload icon" />
			</Button>
		</>);
	} else if (!processingAnswer) {
		mainContent = (<>
			<h1 className='text-4xl text-center mb-5'>
				<img className='inline-block w-14 h-14' src='/hintings_logo_green.png' alt='hintings logo' />{' '}
				hintings
			</h1>
			<div className='xl:absolute xl:top-20 xl:right-20 mb-5'>
				<h4 className='hidden xl:block text-lg font-bold text-center mb-3 text-white'>
					Documents
				</h4>
				<div className='flex flex-col items-center sm:items-start sm:flex-row sm:flex-wrap sm:justify-between xl:block max-h-96 overflow-y-auto'>
					{uploadedFilesJSX}
				</div>
				<div>
					<Button 
						className='text-white px-5 py-2 rounded-full ml-auto xl:mx-auto block' bg='green'
						onClick={() => setShowUploadOverlay(true)}
					>
						upload{' '}
						<img className='inline-block w-5 h-5' src={UploadIcon} alt="Upload icon" />
					</Button>
				</div>
			</div>
			<form onSubmit={handleSubmit} className='relative mb-10'>
				<input
					className={'px-5 py-3 w-full rounded-full shadow-md ' + s['border-gray']}
					placeholder='ask anything...'
					value={question}
					onChange={e => setQuestion(e.target.value)}
					type="text" 
				/>
				<Button 
					bg='green'
					className='absolute top-2 right-2 w-8 h-8 text-white rounded-full pt-[0.1rem]'
					onClick={() => {
						//console.log("i pressed the button");
						handleSubmit;
					}}>
					<FontAwesomeIcon icon={faArrowRight} />
				</Button>
			</form>
			{
				answer ?
					<div>
						<div className='mb-14'>
							<h4 className='mb-2 text-2xl font-bold text-white'>{answer.question}</h4>
							<p>{answer.answer}</p>
						</div>
						<hr className='mb-5' />
						<div>
							<h4 className='mb-2 text-2xl font-bold text-white'>
								Sources
							</h4>
							<ul>
								{sourcesJSX}
							</ul>
						</div>
					</div>
					:
					null
			}
		</>);
	} else {
		mainContent = (<>
			<h4 className="mb-3 text-xl text-center font-bold text-white">Generating Answer</h4>
			<Loading />
			<p className="text-center mt-3 text-white">This can take a minute</p>
		</>);
	}

	return (
		<main className='pt-10 sm:pt-20 relative'>
			<div className='container mx-auto px-5 max-w-xl'>
				{mainContent}
				<UploadOverlay show={showUploadOverlay} onUploadSuccess={files => {
					setUploadedFiles(files);
					setShowUploadOverlay(false);
				}} />
				<SourceDocOverlay 
					show={showSourceOverlay}
					source={viewedSource}
					onClose={() => setShowSourceOverlay(false)}
				/>
			</div>
		</main>
	);
}

export default IndexPage;
