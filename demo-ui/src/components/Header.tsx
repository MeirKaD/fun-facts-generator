export function Header() {
  return (
    <header className="relative z-20 w-full overflow-visible">
      <div className="glass-card border-0 border-b border-white/20 rounded-none backdrop-blur-xl bg-white/5">
        <div className="container mx-auto px-1 py-2">
          <div className="flex items-center justify-between h-16">
            {/* Left side - Small logo */}
            <div className="flex items-center">
              <img 
                src="https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/dark/llamaindex-color.png" 
                alt="LlamaIndex"
                className="w-12 h-12 object-contain hover:scale-105 transition-transform"
              />
            </div>

            {/* Center - Main Bright Data logo and title */}
            <div className="flex flex-col items-center gap-1 relative h-16 w-64">
              <img 
                src="https://proxyway.com/wp-content/uploads/2022/05/bright-data-logo.png?ver=1704718964" 
                alt="Bright Data"
                className="w-64 h-64 object-contain hover:scale-105 transition-transform brightness-125 contrast-125 saturate-150 drop-shadow-2xl"
              />
            </div>

            {/* Right side - Small logo */}
            <div className="flex items-center">
              <img 
                src="https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/ai21-brand-color.png" 
                alt="AI21"
                className="w-12 h-12 object-contain hover:scale-105 transition-transform"
              />
            </div>

            
          </div>
        </div>
      </div>

      {/* Subtle glow effect */}
      <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-96 h-1 bg-gradient-to-r from-transparent via-white/40 to-transparent"></div>
    </header>
  )
}