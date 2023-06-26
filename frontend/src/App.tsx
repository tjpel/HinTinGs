import Footer from "./components/footer";
import Navbar from "./components/navbar";
import IndexPage from "./pages";

// routing here in the future
function App() {
	return (
		<>
			<div className="pb-20 md:pb-0 md:min-h-screen">
				<Navbar />
				<IndexPage />
			</div>
			<Footer />
		</>
	);
}

export default App;
