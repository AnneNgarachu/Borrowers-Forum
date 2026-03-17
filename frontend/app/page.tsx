import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Calculator,
  Search,
  Globe,
  TrendingUp,
  FileText,
  BarChart3,
  Shield,
  Leaf,
  Users,
  ArrowRight,
  ChevronRight,
  BookOpen,
} from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <Header />

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 md:py-24">
        <div className="max-w-4xl mx-auto text-center space-y-6">
          <h1 className="text-4xl md:text-6xl font-bold text-balance">
            Debt Intelligence for{" "}
            <span className="bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">
              Developing Nations
            </span>
          </h1>
          <p className="text-xl text-slate-600 text-balance max-w-3xl mx-auto">
            Verified precedents, economic analysis, and research tools supporting sustainable debt solutions. Built on
            data from IMF, World Bank, and Paris Club sources.
          </p>
          <div className="flex flex-wrap gap-4 justify-center pt-4">
            <Link href="/calculator">
              <Button
                size="lg"
                className="bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 text-white shadow-lg shadow-blue-500/30"
              >
                <Calculator className="mr-2 h-5 w-5" />
                Calculate Debt Impact
              </Button>
            </Link>
            <Link href="/precedents">
              <Button size="lg" variant="outline" className="border-2 border-blue-200 hover:bg-blue-50 bg-transparent">
                <Search className="mr-2 h-5 w-5" />
                Explore Precedents
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 max-w-6xl mx-auto">
          <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">
                16
              </CardTitle>
              <CardDescription className="text-slate-600">Countries Covered</CardDescription>
              <p className="text-xs text-slate-500 mt-1">500M+ people represented</p>
            </CardHeader>
          </Card>
          <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">
                29
              </CardTitle>
              <CardDescription className="text-slate-600">Verified Cases</CardDescription>
              <p className="text-xs text-slate-500 mt-1">2005-2024 precedents</p>
            </CardHeader>
          </Card>
          <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">
                12
              </CardTitle>
              <CardDescription className="text-slate-600">Climate-Linked Deals</CardDescription>
              <p className="text-xs text-slate-500 mt-1">Debt + climate provisions</p>
            </CardHeader>
          </Card>
          <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">
                $450B+
              </CardTitle>
              <CardDescription className="text-slate-600">Debt Restructured</CardDescription>
              <p className="text-xs text-slate-500 mt-1">Total across all cases</p>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* Why This Matters Section */}
      <section className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-gradient-to-br from-slate-50 to-blue-50/50 border-slate-200 shadow-lg">
            <CardHeader className="text-center pb-4">
              <CardTitle className="text-2xl font-bold">Why This Platform Exists</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-slate-700 leading-relaxed">
                When creditors negotiate debt restructuring, they share data and coordinate strategies with each other.
                Countries in debt often negotiate alone—without knowing what terms similar countries achieved or what's
                realistic to ask for.
              </p>
              <p className="text-slate-700 leading-relaxed">
                This platform provides that missing information: verified historical cases, economic data, and tools to
                model different scenarios.
              </p>
              <p className="text-slate-700 leading-relaxed font-medium">
                The 16 countries in this database represent over 500 million people and $1.2 trillion in combined GDP.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Database Coverage Section */}
      <section className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <Card className="bg-gradient-to-br from-slate-50 to-blue-50/30 border-slate-200 shadow-sm">
            <CardHeader className="pb-4">
              <CardTitle className="text-2xl font-bold text-center">Database Coverage</CardTitle>
              <CardDescription className="text-center text-slate-600">
                Comprehensive verified data from official sources
              </CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm font-semibold text-slate-700">
                  <Globe className="h-4 w-4 text-blue-600" />
                  Regions Covered
                </div>
                <ul className="text-sm text-slate-600 space-y-1 ml-6">
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>Sub-Saharan Africa</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>South Asia</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>Latin America & Caribbean</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>Middle East & North Africa</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>Europe & Central Asia</span>
                  </li>
                </ul>
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm font-semibold text-slate-700">
                  <FileText className="h-4 w-4 text-blue-600" />
                  Years Covered
                </div>
                <div className="text-sm text-slate-600 space-y-1 ml-6">
                  <div className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>2005-2024 (20 years)</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>Multilateral restructurings</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>HIPC Initiative</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>Common Framework</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>Recent restructurings</span>
                  </div>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm font-semibold text-slate-700">
                  <Shield className="h-4 w-4 text-blue-600" />
                  Official Sources
                </div>
                <ul className="text-sm text-slate-600 space-y-1 ml-6">
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>IMF Staff Reports & Press Releases</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>Paris Club Official Reports</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>World Bank Debt Reports</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>World Bank WDI Database</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    <span>ND-GAIN Climate Index</span>
                  </li>
                </ul>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Recent Additions Section */}
      <section className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-8">
            <h2 className="text-2xl md:text-3xl font-bold mb-2">Recent Additions</h2>
            <p className="text-slate-600">Latest precedents added to our database</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Zambia 2023 */}
            <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <CardTitle className="text-xl font-bold">Zambia</CardTitle>
                    <CardDescription className="text-slate-600">2023 • Common Framework</CardDescription>
                  </div>
                  <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    <Leaf className="h-3 w-3 mr-1" />
                    Climate: Yes
                  </span>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-bold text-[#1e3a5f] mb-4">$6.3B</p>
                <Link href="/precedents">
                  <Button variant="outline" className="w-full group bg-transparent">
                    View Details
                    <ChevronRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Ukraine 2024 */}
            <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1">
              <CardHeader className="pb-3">
                <div className="flex items-start gap-2 mb-2">
                  <div>
                    <CardTitle className="text-xl font-bold">Ukraine</CardTitle>
                    <CardDescription className="text-slate-600">2024 • Wartime Restructuring</CardDescription>
                  </div>
                  <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-700">
                    Climate: No
                  </span>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-bold text-[#1e3a5f] mb-4">$20B</p>
                <Link href="/precedents">
                  <Button variant="outline" className="w-full group bg-transparent">
                    View Details
                    <ChevronRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Ecuador 2023 */}
            <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <CardTitle className="text-xl font-bold">Ecuador</CardTitle>
                    <CardDescription className="text-slate-600">2023 • Debt-for-Nature</CardDescription>
                  </div>
                  <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    <Leaf className="h-3 w-3 mr-1" />
                    Climate: Yes
                  </span>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-bold text-[#1e3a5f] mb-4">$1.6B</p>
                <Link href="/precedents">
                  <Button variant="outline" className="w-full group bg-transparent">
                    View Details
                    <ChevronRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Comprehensive Debt Analysis Platform</h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Everything you need to make informed debt restructuring decisions
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Debt Calculator Feature */}
            <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-blue-400 flex items-center justify-center mb-4 shadow-lg shadow-blue-500/30">
                  <Calculator className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-xl">Debt Relief Impact Calculator</CardTitle>
                <CardDescription className="text-slate-600">
                  Convert debt service savings into tangible outcomes
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-2 text-sm text-slate-600">
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                  <span>Healthcare: Doctors employed for 1 or 5 years</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                  <span>Education: Schools that could be built</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                  <span>Climate: % of annual adaptation budget</span>
                </div>
                <Link href="/calculator">
                  <Button className="w-full mt-4 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600">
                    Start Calculating
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Precedents Search Feature */}
            <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-blue-400 flex items-center justify-center mb-4 shadow-lg shadow-blue-500/30">
                  <Search className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-xl">Verified Precedents</CardTitle>
                <CardDescription className="text-slate-600">Search 29 historical restructuring cases</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2 text-sm text-slate-600">
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                  <span>Advanced filtering by creditor and treatment type</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                  <span>AI-powered similarity scoring (60-100% matches)</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                  <span>12 climate-linked restructuring cases</span>
                </div>
                <Link href="/precedents">
                  <Button className="w-full mt-4 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600">
                    Explore Precedents
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Country Profiles Feature */}
            <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-blue-400 flex items-center justify-center mb-4 shadow-lg shadow-blue-500/30">
                  <Globe className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-xl">Country Profiles</CardTitle>
                <CardDescription className="text-slate-600">Live economic and climate data</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2 text-sm text-slate-600">
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                  <span>Real-time World Bank economic indicators</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                  <span>Climate vulnerability scoring and analysis</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                  <span>16 debt-stressed countries covered</span>
                </div>
                <Link href="/countries">
                  <Button className="w-full mt-4 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600">
                    View Countries
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Who This Is For Section */}
      <section className="container mx-auto px-4 py-16 bg-gradient-to-br from-blue-50/50 to-slate-50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Who This Is For</h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Professional tools designed for debt negotiators, policymakers, and researchers
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Finance Ministers */}
            <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1">
              <CardHeader className="pb-4">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-blue-400 flex items-center justify-center shadow-lg shadow-blue-500/30">
                    <TrendingUp className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-xl mb-2">Finance Ministers</CardTitle>
                    <p className="text-sm text-slate-600 leading-relaxed">
                      Analyze restructuring options using 29 verified precedents and live economic data to inform
                      evidence-based policy decisions
                    </p>
                  </div>
                </div>
              </CardHeader>
            </Card>

            {/* Debt Negotiators */}
            <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1">
              <CardHeader className="pb-4">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-blue-400 flex items-center justify-center shadow-lg shadow-blue-500/30">
                    <Users className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-xl mb-2">Debt Negotiators</CardTitle>
                    <p className="text-sm text-slate-600 leading-relaxed">
                      Understand achievable terms by examining comparable country profiles, creditor compositions, and
                      documented outcomes
                    </p>
                  </div>
                </div>
              </CardHeader>
            </Card>

            {/* Policy Researchers */}
            <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1">
              <CardHeader className="pb-4">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-blue-400 flex items-center justify-center shadow-lg shadow-blue-500/30">
                    <BarChart3 className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-xl mb-2">Policy Researchers</CardTitle>
                    <p className="text-sm text-slate-600 leading-relaxed">
                      Access comprehensive debt-climate analysis with verified data from Paris Club, IMF HIPC documents,
                      and World Bank publications
                    </p>
                  </div>
                </div>
              </CardHeader>
            </Card>

            {/* Development Economists */}
            <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1">
              <CardHeader className="pb-4">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-blue-400 flex items-center justify-center shadow-lg shadow-blue-500/30">
                    <BookOpen className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-xl mb-2">Development Economists</CardTitle>
                    <p className="text-sm text-slate-600 leading-relaxed">
                      Model fiscal sustainability scenarios with climate-adjusted frameworks and economic vulnerability
                      indicators
                    </p>
                  </div>
                </div>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-gradient-to-r from-blue-600 to-blue-500 border-0 text-white shadow-2xl shadow-blue-500/30">
            <CardHeader className="text-center pb-6">
              <CardTitle className="text-3xl md:text-4xl font-bold mb-4">Ready to Explore Your Options?</CardTitle>
              <CardDescription className="text-blue-50 text-lg">
                Start analyzing debt relief scenarios and discover what your country could gain
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-wrap gap-4 justify-center">
              <Link href="/calculator">
                <Button size="lg" className="bg-white text-blue-600 hover:bg-blue-50 shadow-lg">
                  <Calculator className="mr-2 h-5 w-5" />
                  Calculate Your Country's Potential
                </Button>
              </Link>
              <Link href="/api-docs">
                <Button
                  size="lg"
                  variant="outline"
                  className="border-2 border-white text-white hover:bg-white/10 bg-transparent"
                >
                  <FileText className="mr-2 h-5 w-5" />
                  API Documentation
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </section>

      <Footer />
    </div>
  )
}
