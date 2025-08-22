import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import AnalyzeImage from './pages/AnalyzeImage'
import AnalyzeText from './pages/AnalyzeText'
import AnalysisResult from './pages/AnalysisResult'
import Gallery from './pages/Gallery'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="analyze/image" element={<AnalyzeImage />} />
        <Route path="analyze/text" element={<AnalyzeText />} />
        <Route path="analysis/:id" element={<AnalysisResult />} />
        <Route path="gallery" element={<Gallery />} />
      </Route>
    </Routes>
  )
}

export default App
