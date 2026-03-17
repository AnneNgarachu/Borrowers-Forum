import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { Breadcrumbs } from "@/components/breadcrumbs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ExternalLink, Book, Code, Database, Shield, Zap, Info, Mail } from "lucide-react"
import Link from "next/link"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

export default function ApiDocsPage() {
  const contactEmail = process.env.NEXT_PUBLIC_ADMIN_EMAIL || "admin@borrowersforum.org"

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <Header />

      <div className="container mx-auto px-4 py-12 max-w-6xl">
        <Breadcrumbs />

        <div className="mb-12 text-center">
          <div className="flex items-center justify-center gap-3 mb-4">
            <h1 className="text-4xl md:text-5xl font-bold">
              API{" "}
              <span className="bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">
                Documentation
              </span>
            </h1>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger>
                  <Info className="h-5 w-5 text-muted-foreground" />
                </TooltipTrigger>
                <TooltipContent className="max-w-xs">
                  <p>Complete API reference for integrating with The Borrower's Forum Platform</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto mb-6">
            Complete reference for The Borrower's Forum Platform API
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            <a href="https://borrowers-forum.onrender.com/api/docs" target="_blank" rel="noopener noreferrer">
              <Button
                size="lg"
                className="bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600"
              >
                <ExternalLink className="mr-2 h-5 w-5" />
                Interactive API Docs
              </Button>
            </a>
            <a href="https://borrowers-forum.onrender.com" target="_blank" rel="noopener noreferrer">
              <Button size="lg" variant="outline" className="border-2 border-blue-200 hover:bg-blue-50 bg-transparent">
                <Zap className="mr-2 h-5 w-5" />
                API Base URL
              </Button>
            </a>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          <Card className="bg-white/80 backdrop-blur text-center p-4">
            <div className="text-2xl font-bold text-blue-600">19</div>
            <div className="text-sm text-slate-600">Total Endpoints</div>
          </Card>
          <Card className="bg-white/80 backdrop-blur text-center p-4">
            <div className="text-2xl font-bold text-blue-600">190+</div>
            <div className="text-sm text-slate-600">Countries</div>
          </Card>
          <Card className="bg-white/80 backdrop-blur text-center p-4">
            <div className="text-2xl font-bold text-blue-600">Live</div>
            <div className="text-sm text-slate-600">World Bank Data</div>
          </Card>
          <Card className="bg-white/80 backdrop-blur text-center p-4">
            <div className="text-2xl font-bold text-blue-600">Secure</div>
            <div className="text-sm text-slate-600">API Key Auth</div>
          </Card>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          <Card className="bg-white/80 backdrop-blur">
            <CardHeader>
              <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-blue-400 flex items-center justify-center mb-4">
                <Database className="h-6 w-6 text-white" />
              </div>
              <CardTitle>Base URL</CardTitle>
              <CardDescription>Production API endpoint</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="bg-slate-100 p-4 rounded-lg font-mono text-sm mb-4">
                https://borrowers-forum.onrender.com
              </div>
              <p className="text-sm text-slate-600">
                All API requests should be made to this base URL. The API is live and operational 24/7.
              </p>
            </CardContent>
          </Card>

          <Card className="bg-white/80 backdrop-blur">
            <CardHeader>
              <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-blue-400 flex items-center justify-center mb-4">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <CardTitle>Authentication</CardTitle>
              <CardDescription>API key required for protected endpoints</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="bg-slate-100 p-4 rounded-lg font-mono text-sm mb-4">X-API-Key: your_api_key_here</div>
              <p className="text-sm text-slate-600">
                Include your API key in the request header. Contact the administrator to obtain an API key.
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <h2 className="text-3xl font-bold mb-6">API Endpoints</h2>

          <Card className="bg-white/80 backdrop-blur">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <div className="w-8 h-8 rounded bg-blue-100 flex items-center justify-center">
                  <Code className="h-4 w-4 text-blue-600" />
                </div>
                Countries API
              </CardTitle>
              <CardDescription>Access country profiles and economic data</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex items-center gap-2 mb-1">
                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded">GET</span>
                  <code className="text-sm font-mono">/api/v1/countries</code>
                </div>
                <p className="text-sm text-slate-600">List all countries with profiles</p>
              </div>
              <div className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex items-center gap-2 mb-1">
                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded">GET</span>
                  <code className="text-sm font-mono">/api/v1/countries/:code</code>
                </div>
                <p className="text-sm text-slate-600">Get specific country by ISO code</p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/80 backdrop-blur">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <div className="w-8 h-8 rounded bg-blue-100 flex items-center justify-center">
                  <Code className="h-4 w-4 text-blue-600" />
                </div>
                Debt Calculator API
              </CardTitle>
              <CardDescription>Calculate opportunity costs of debt relief</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex items-center gap-2 mb-1">
                  <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded">POST</span>
                  <code className="text-sm font-mono">/api/v1/debt/calculate</code>
                </div>
                <p className="text-sm text-slate-600">Calculate healthcare, education, and climate equivalents</p>
              </div>
              <div className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex items-center gap-2 mb-1">
                  <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded">POST</span>
                  <code className="text-sm font-mono">/api/v1/debt/calculate-live</code>
                </div>
                <p className="text-sm text-slate-600">Calculate using live World Bank data</p>
              </div>
              <div className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex items-center gap-2 mb-1">
                  <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded">POST</span>
                  <code className="text-sm font-mono">/api/v1/debt/compare</code>
                </div>
                <p className="text-sm text-slate-600">Compare multiple relief scenarios</p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/80 backdrop-blur">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <div className="w-8 h-8 rounded bg-blue-100 flex items-center justify-center">
                  <Code className="h-4 w-4 text-blue-600" />
                </div>
                Precedents API
              </CardTitle>
              <CardDescription>Search historical debt restructuring cases</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex items-center gap-2 mb-1">
                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded">GET</span>
                  <code className="text-sm font-mono">/api/v1/precedents</code>
                </div>
                <p className="text-sm text-slate-600">Search with filters (country, year, creditor, treatment)</p>
              </div>
              <div className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex items-center gap-2 mb-1">
                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded">GET</span>
                  <code className="text-sm font-mono">/api/v1/precedents/similar</code>
                </div>
                <p className="text-sm text-slate-600">AI-powered similarity matching (0-100 score)</p>
              </div>
              <div className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex items-center gap-2 mb-1">
                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded">GET</span>
                  <code className="text-sm font-mono">/api/v1/precedents/stats</code>
                </div>
                <p className="text-sm text-slate-600">Get aggregated statistics by type</p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white/80 backdrop-blur">
            <CardHeader>
              <div className="w-8 h-8 rounded bg-blue-100 flex items-center justify-center">
                <Code className="h-4 w-4 text-blue-600" />
              </div>
              <CardTitle className="flex items-center gap-2">Live Data API</CardTitle>
              <CardDescription>Real-time World Bank data integration</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex items-center gap-2 mb-1">
                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded">GET</span>
                  <code className="text-sm font-mono">/api/v1/live/economic/:code</code>
                </div>
                <p className="text-sm text-slate-600">Live economic indicators (GDP, population, debt)</p>
              </div>
              <div className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex items-center gap-2 mb-1">
                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded">GET</span>
                  <code className="text-sm font-mono">/api/v1/live/countries</code>
                </div>
                <p className="text-sm text-slate-600">List all 190+ supported countries</p>
              </div>
            </CardContent>
          </Card>
        </div>

        <Card className="mt-12 bg-white/80 backdrop-blur">
          <CardHeader>
            <div className="flex items-center gap-2">
              <CardTitle>Example Request</CardTitle>
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger>
                    <Info className="h-4 w-4 text-muted-foreground" />
                  </TooltipTrigger>
                  <TooltipContent className="max-w-xs">
                    <p>Copy and paste this cURL command to test the debt calculator API endpoint</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </div>
            <CardDescription>Calculate debt relief impact for Ghana</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="bg-slate-900 text-slate-100 p-6 rounded-lg font-mono text-sm overflow-x-auto">
              <div className="text-blue-400 mb-2"># Calculate debt opportunity costs</div>
              <div className="text-slate-300">curl -X POST \</div>
              <div className="text-slate-300 ml-4">"https://borrowers-forum.onrender.com/api/v1/debt/calculate" \</div>
              <div className="text-slate-300 ml-4">-H "Content-Type: application/json" \</div>
              <div className="text-slate-300 ml-4">-H "X-API-Key: your_api_key_here" \</div>
              <div className="text-slate-300 ml-4">-d '&#123;</div>
              <div className="text-slate-300 ml-8">"country_code": "GHA",</div>
              <div className="text-slate-300 ml-8">"year": 2023,</div>
              <div className="text-slate-300 ml-8">"debt_amount_usd": 50000000</div>
              <div className="text-slate-300 ml-4">&#125;'</div>
            </div>
          </CardContent>
        </Card>

        <div className="mt-12 grid md:grid-cols-3 gap-6">
          <Card className="bg-gradient-to-br from-blue-50 to-white">
            <CardHeader>
              <Book className="h-8 w-8 text-blue-600 mb-2" />
              <CardTitle className="text-lg">Full Documentation</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-slate-600 mb-4">
                Comprehensive API reference with all endpoints, parameters, and examples.
              </p>
              <a href="https://borrowers-forum.onrender.com/api/docs" target="_blank" rel="noopener noreferrer">
                <Button variant="outline" className="w-full bg-transparent">
                  View Docs
                  <ExternalLink className="ml-2 h-4 w-4" />
                </Button>
              </a>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-blue-50 to-white">
            <CardHeader>
              <Database className="h-8 w-8 text-blue-600 mb-2" />
              <CardTitle className="text-lg">Data Sources</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-slate-600 mb-4">World Bank, IMF, and Paris Club official data sources.</p>
              <Link href="/countries">
                <Button variant="outline" className="w-full bg-transparent">
                  View Data
                </Button>
              </Link>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-blue-50 to-white">
            <CardHeader>
              <Shield className="h-8 w-8 text-blue-600 mb-2" />
              <CardTitle className="text-lg">Get API Key</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-slate-600 mb-4">Contact the administrator to request your secure API key.</p>
              <a
                href={`mailto:${contactEmail}?subject=API Key Request - The Borrower's Forum&body=Hello,%0D%0A%0D%0AI would like to request an API key for The Borrower's Forum Platform.%0D%0A%0D%0AName:%0D%0AOrganization:%0D%0APurpose:%0D%0A%0D%0AThank you.`}
              >
                <Button variant="outline" className="w-full bg-transparent">
                  <Mail className="mr-2 h-4 w-4" />
                  Contact Admin
                </Button>
              </a>
            </CardContent>
          </Card>
        </div>
      </div>

      <Footer />
    </div>
  )
}
