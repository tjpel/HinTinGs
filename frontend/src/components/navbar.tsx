import s from '../styles/navbar.module.scss';
import Link from './link';

function Navbar() {
	return (
		<div className={'px-8 sm:px-20 flex flex-row justify-between flex-nowrap items-center' + s.nav}>
			<img className='grow-0 w-14 h-14' src="/hintings_logo_green.png" alt="hintings logo" />
			<nav className='py-5'>
				<Link href='#' text='about' className='mr-10' />
				<Link href='#' text='contact us'/>
			</nav>
		</div>
	);
}

export default Navbar;
