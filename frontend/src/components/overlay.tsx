import s from '../styles/overlay.module.scss';

type Props = {
	children: JSX.Element | JSX.Element[],
	className?: string,
	show: boolean
};

function Overlay({ children, className, show }: Props) {
	return (
		<div className={s['overlay-container'] + ' ' + (show ? s.show : '')}>
			<div className={(className ? className : '')}>
				{children}
			</div>
		</div>
	);
}

export default Overlay;
