import { Palette } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          {/* Logo and description */}
          <div className="flex items-center space-x-2 mb-4 md:mb-0">
            <div className="w-6 h-6 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center">
              <Palette className="w-4 h-4 text-white" />
            </div>
            <span className="text-lg font-bold text-gradient">Artell</span>
          </div>
          
          <p className="text-gray-600 text-sm text-center md:text-left">
            Descubra o significado das obras de arte através da inteligência artificial
          </p>
          
          {/* Links */}
          <div className="flex space-x-6 mt-4 md:mt-0">
            <a href="#" className="text-gray-600 hover:text-primary-600 text-sm transition-colors duration-200">
              Sobre
            </a>
            <a href="#" className="text-gray-600 hover:text-primary-600 text-sm transition-colors duration-200">
              Privacidade
            </a>
            <a href="#" className="text-gray-600 hover:text-primary-600 text-sm transition-colors duration-200">
              Termos
            </a>
          </div>
        </div>
        
        <div className="mt-8 pt-8 border-t border-gray-200 text-center">
          <p className="text-gray-500 text-sm">
            © 2024 Artell. Todos os direitos reservados.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
