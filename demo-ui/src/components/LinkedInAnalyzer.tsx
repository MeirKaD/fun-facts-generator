import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import ReactMarkdown from 'react-markdown'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from './ui/form'
import { Loader2, Sparkles, Users, LinkIcon } from 'lucide-react'
import { Header } from './Header'

const formSchema = z.object({
  url1: z.string().min(1, 'URL is required').refine(
    (url) => url.includes('linkedin.com/in/'),
    'Must be a valid LinkedIn profile URL'
  ),
  url2: z.string().min(1, 'URL is required').refine(
    (url) => url.includes('linkedin.com/in/'),
    'Must be a valid LinkedIn profile URL'
  ),
  url3: z.string().min(1, 'URL is required').refine(
    (url) => url.includes('linkedin.com/in/'),
    'Must be a valid LinkedIn profile URL'
  ),
})

type FormData = z.infer<typeof formSchema>

interface Profile {
  profile_url: string
  name: string
  headline: string
  funny_facts: string[]
}

interface AnalysisResult {
  status: string
  profiles_analyzed: number
  results: Profile[]
}

export function LinkedInAnalyzer() {
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      url1: '',
      url2: '',
      url3: '',
    },
  })

  const onSubmit = async (data: FormData) => {
    setIsLoading(true)
    setError(null)
    setResults(null)

    try {
      const response = await fetch('http://localhost:8000/analyze-profiles', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          urls: [data.url1, data.url2, data.url3]
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Analysis failed')
      }

      const result: AnalysisResult = await response.json()
      setResults(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen w-full relative">
      <Header />
      <div className="min-h-screen w-full backdrop-blur-sm bg-black/10 pt-8">
        <div className="container mx-auto px-4 py-12 max-w-5xl relative z-10">
                        <div className="text-center">
                <h1 className="text-2xl font-bold text-white drop-shadow-lg py-4">
                  LinkedIn Profile Analyzer
                </h1>
              </div>
          <div className="text-center mb-12">
            <p className="text-xl text-white/90 max-w-3xl mx-auto drop-shadow">
              Discover hilarious and insightful facts about LinkedIn profiles using AI. 
              Enter three LinkedIn URLs and let our AI generate entertaining observations.
            </p>
          </div>

          <div className="glass-card mb-12 rounded-3xl overflow-hidden">
            <CardContent className="p-8">
              <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                  <div className="grid gap-6">
                    {['url1', 'url2', 'url3'].map((fieldName, index) => (
                      <FormField
                        key={fieldName}
                        control={form.control}
                        name={fieldName as keyof FormData}
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel className="text-white font-semibold text-lg">
                              LinkedIn URL {index + 1}
                            </FormLabel>
                            <FormControl>
                              <Input
                                placeholder="https://www.linkedin.com/in/username"
                                {...field}
                                className="h-14 text-lg glass-input text-white placeholder:text-white/60 border-white/30"
                              />
                            </FormControl>
                            <FormMessage className="text-red-300" />
                          </FormItem>
                        )}
                      />
                    ))}
                  </div>
                  
                  <Button 
                    type="submit" 
                    disabled={isLoading}
                    className="w-full h-16 text-xl font-semibold glass-button text-white border-white/40 hover:bg-white/20 rounded-2xl"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-3 h-6 w-6 animate-spin" />
                        Analyzing Profiles...
                      </>
                    ) : (
                      <>
                        
                        Generate Funny Facts
                      </>
                    )}
                  </Button>
                </form>
              </Form>
            </CardContent>
          </div>

          {error && (
            <div className="glass-card mb-8 rounded-2xl border-red-300/50">
              <CardContent className="p-6">
                <div className="flex items-center gap-2 text-red-100">
                  <span className="font-medium">Error:</span>
                  <span>{error}</span>
                </div>
              </CardContent>
            </div>
          )}

          {results && (
            <div className="space-y-8">
              <div className="text-center">
                <h2 className="text-3xl font-bold text-white mb-3 drop-shadow">
                  Analysis Results
                </h2>
                <p className="text-white/90 text-lg">
                  Here are the funny facts generated for each profile
                </p>
              </div>

              <div className="grid gap-8">
                {results.results.map((profile, index) => (
                  <div key={index} className="glass-card rounded-3xl overflow-hidden">
                    <CardHeader className="bg-white/10 backdrop-blur-sm p-8">
                      <div className="flex items-start gap-6">
                        <div className="flex-shrink-0">
                          <div className="w-16 h-16 bg-gradient-to-r from-blue-400 to-purple-400 rounded-2xl flex items-center justify-center backdrop-blur-sm">
                            <Users className="h-8 w-8 text-white" />
                          </div>
                        </div>
                        <div className="flex-1">
                          <CardTitle className="text-2xl font-bold text-white mb-2">
                            {profile.name}
                          </CardTitle>
                          <CardDescription className="text-white/80 text-lg mb-3">
                            {profile.headline}
                          </CardDescription>
                          <a 
                            href={profile.profile_url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-blue-200 hover:text-blue-100 font-medium inline-block"
                          >
                            View LinkedIn Profile →
                          </a>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="p-8">
                      <h4 className="font-semibold text-white mb-6 flex items-center gap-3 text-xl">
                        <Sparkles className="h-5 w-5 text-yellow-300" />
                        Funny Facts
                      </h4>
                      <div className="space-y-4">
                        {profile.funny_facts.map((fact, factIndex) => (
                          <div 
                            key={factIndex}
                            className="flex items-start gap-4 p-6 bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20"
                          >
                            <span className="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full flex items-center justify-center text-white font-bold">
                              {factIndex + 1}
                            </span>
                            <div className="text-white leading-relaxed text-lg prose prose-invert max-w-none">
                              <ReactMarkdown 
                                components={{
                                  p: ({children}) => <p className="mb-0">{children}</p>,
                                  strong: ({children}) => <strong className="text-yellow-300 font-bold">{children}</strong>
                                }}
                              >
                                {fact}
                              </ReactMarkdown>
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}