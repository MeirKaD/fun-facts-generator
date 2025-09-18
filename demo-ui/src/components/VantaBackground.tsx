import { useEffect, useRef } from 'react'

interface VantaBackgroundProps {
  children: React.ReactNode
}

export function VantaBackground({ children }: VantaBackgroundProps) {
  const vantaRef = useRef<HTMLDivElement>(null)
  const vantaEffect = useRef<any>(null)

  useEffect(() => {
    const loadVanta = async () => {
      try {
        // Dynamically import THREE and VANTA
        const THREE = await import('three')
        const VANTA = await import('vanta/dist/vanta.fog.min.js')
        
        // Make THREE available globally for Vanta
        ;(window as any).THREE = THREE

        if (vantaRef.current && !vantaEffect.current) {
          vantaEffect.current = (VANTA as any).default.FOG({
            el: vantaRef.current,
            THREE: THREE,
            mouseControls: true,
            touchControls: true,
            gyroControls: false,
            minHeight: 200.00,
            minWidth: 200.00,
            highlightColor: 0x6366f1, // Indigo
            midtoneColor: 0x8b5cf6, // Purple
            baseColor: 0xec4899, // Pink
            speed: 0.8,
            zoom: 0.7
          })
        }
      } catch (error) {
        console.error('Failed to load Vanta.js:', error)
      }
    }

    loadVanta()

    return () => {
      if (vantaEffect.current) {
        vantaEffect.current.destroy()
        vantaEffect.current = null
      }
    }
  }, [])

  return (
    <div 
      ref={vantaRef} 
      className="fixed inset-0 w-full h-full z-0"
      style={{ zIndex: -1 }}
    >
      <div className="absolute inset-0 z-10">
        {children}
      </div>
    </div>
  )
}