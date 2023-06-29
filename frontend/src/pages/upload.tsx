import { useRef, useState } from "react";
import Button from "../components/button";
import Overlay from "../components/overlay";
import { protectedFetch, API_URL } from '../utils/fetch';
import UploadDarkIcon from '../assets/upload_dark.svg';
import IngestIcon from '../assets/ingest.svg';
import s from '../styles/index.module.scss';
import Loading from "../components/loading";

type Props = {
	show: boolean,
	onUploadSuccess: (files: File[]) => void
};

const ALLOWED_FILES = ['text/plain', 'text/markdown'];

function UploadOverlay({ show, onUploadSuccess }: Props) {
	const [files, setFiles] = useState<File[]>([]);
	const [processingUpload, setProcessingUpload] = useState(false);

	const FileInput = useRef<HTMLInputElement>(null);
	//console.log("VITE_API_URL is " + import.meta.env.VITE_API_URL);
	//console.log("API URL is " + API_URL);

	const filesJSX = [];
	if (files.length) {
		for (let i = 0; i < files.length; i++) {
			const file = files[i];
			filesJSX.push(
				<li className='mb-3 flex flex-row' key={i}>
					<span 
						className={'mt-[0.35rem] w-3 h-3 rounded-full inline-block align-middle mr-3 ' + s['bg-dot-gray']} 
					/>
					<span className='inline-block'>
						{file.name}
					</span>
				</li>
			);
		}
	}

	const onUploadFiles = () => {
		setProcessingUpload(true);
		const url = API_URL + '/documents/';
		console.log(url);
		const form = new FormData();
		for (let i = 0; i < files.length; i++) {
			form.append('files', files[i]);
		}
		const options = {
			method: 'POST',
			body: form
		};
		console.log('Uploading files to server');
		console.log(files);		
		protectedFetch(url, options).then(() => {
			onUploadSuccess(files);
			setFiles([]);
			setProcessingUpload(false);
		}).catch(err => {
			setProcessingUpload(false);
			console.log('An error occurred while uploading your files');
			console.log("URL: " + url);
			console.log("Options: " + options.toString());
			alert((err.message ? err.message : JSON.stringify(err)));
		});
	};

	let mainContent;
	if (processingUpload) {
		mainContent = (<>
			<h4 className="mb-3 text-xl text-center font-bold">Uploading To Server</h4>
			<Loading />
			<p className="text-center mt-3">Thank you for your patience</p>
		</>);
	} else {
		mainContent = (<>
			<label htmlFor="document-upload">
				<Button 
					className='rounded-full px-5 sm:px-10 py-2 text-black text-lg text-center' bg='gray'
					onClick={() => (FileInput.current as HTMLInputElement).click()}
				>
					upload documents{' '}
					<img className='inline-block w-5 h-5' src={UploadDarkIcon} alt="Upload icon" />
				</Button>
			</label>
			<input 
				ref={FileInput}
				className='hidden' type="file" name="document-upload" id="document-upload" 
				multiple
				onChange={e => {
					const files = e.target.files;
					if (files) {
						const fileArray = [];
						for (let i = 0; i < files.length; i++) {
							const file = files[i];
							if (ALLOWED_FILES.includes(file.type)) {
								fileArray.push(file);
							}
						}
						setFiles(fileArray);
					}
				}}
			/>
			<ul className='mt-10 h-[20rem] overflow-y-auto'>
				{filesJSX}
			</ul>
			{
				files.length > 0 ?
					<Button 
						className='text-white px-5 py-2 rounded-full mx-auto flex flex-row justify-between items-center sm:w-72' 
						bg='green'
						onClick={() => onUploadFiles()}
					>
						<span>ingest documents</span>
						<img className='inline-block w-5 h-5' src={IngestIcon} alt="Ingest document icon" />
					</Button>
					:
					null
			}
		</>);
	}

	return (
		<Overlay show={show} className='max-w-2xl mx-auto px-5'>
			<div className='bg-white py-10 px-5 sm:px-10 rounded-2xl mt-20 md:mt-40'>
				{mainContent}
			</div>
		</Overlay>
	);
}

export default UploadOverlay;
