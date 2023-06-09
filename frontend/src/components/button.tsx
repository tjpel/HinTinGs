import s from '../styles/button.module.scss';

type Props = {
	onClick?: () => void,
	className?: string,
	children: React.ReactNode,
	bg: 'gray' | 'green' | 'orange'
};

const colorMap = {
	gray: s.gray,
	green: s.green,
	orange: s.orange
};

function Button({ onClick, className, children, bg }: Props) {
	return (
		<button 
			className={colorMap[bg] + ' ' + (className ? className : '')}
			onClick={onClick}
		>
			{children}
		</button>
	);
}

export default Button;
