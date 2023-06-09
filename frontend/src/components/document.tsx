import DocumentIcon from '../assets/document.svg';
import TextIcon from '../assets/text_left.svg';
import TrashIcon from '../assets/trash.svg';
import s from '../styles/document.module.scss';
import Button from './button';

type Props = {
	name: string,
	className?: string,
	ext: 'txt' | 'md'
};

function Document({ name, className, ext }: Props) {
	const icon = ext !== 'txt' ? TextIcon : DocumentIcon; 

	return (
		<div className={(className ? className : '') + ' px-3 py-2 rounded-full ' + s['border-gray']}>
			<img className='inline-block w-5 h-5 mr-3' src={icon} alt="Document icon" />
			<p 
				className='inline-block mr-3 text-sm w-32 text-center overflow-x-hidden whitespace-nowrap overflow-ellipsis align-middle'
			>
				{name}
			</p>
			<Button 
				bg="orange" 
				className='w-6 h-6 rounded-full align-middle inline-flex flex-row justify-center items-center' 
			>
				<img className='inline-block w-4 h-4' src={TrashIcon} alt="Remove document" />
			</Button>
		</div>
	);
}

export default Document;
