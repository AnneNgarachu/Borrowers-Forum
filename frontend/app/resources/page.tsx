import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { Breadcrumbs } from "@/components/breadcrumbs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import {
  FileText,
  BookOpen,
  Scale,
  BarChart,
  Database,
  AlertCircle,
  Users,
  Code,
  GitBranch,
  Search,
} from "lucide-react"
import Link from "next/link"

export default function ResourcesPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <Header />

      <div className="container mx-auto px-4 py-12 max-w-6xl">
        <Breadcrumbs />

        <div className="mb-12 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Resources &{" "}
            <span className="bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">Roadmap</span>
          </h1>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto">
            Research library, analytical tools, and open-source development roadmap for debt intelligence infrastructure
          </p>
        </div>

        <Card className="mb-12 bg-gradient-to-br from-blue-50 to-white border-2 border-blue-200">
          <CardHeader>
            <CardTitle className="text-2xl">About This Platform</CardTitle>
            <CardDescription className="text-base text-slate-500">
              A prototype operationalizing digital infrastructure called for by the UN Expert Group on Debt.
              Conceptualized after the COP 30 Simulation Program.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-slate-700 leading-relaxed">
              When countries need to restructure their debt, they often negotiate alone—without data on what terms other
              countries achieved or tools to analyze their options. Meanwhile, the institutions they negotiate with have
              had coordinated systems and shared intelligence since 1956.
            </p>
            <p className="text-slate-700 leading-relaxed font-medium">This platform helps level that playing field.</p>
            <div className="space-y-2">
              <p className="text-slate-700">It provides:</p>
              <ul className="list-disc list-inside text-slate-700 space-y-1 ml-2">
                <li>Verified data from 29 historical restructuring cases</li>
                <li>Economic profiles of 16 countries in active negotiations</li>
                <li>Tools to model debt relief scenarios</li>
              </ul>
            </div>
          </CardContent>
        </Card>

        <Card className="mb-12 bg-gradient-to-br from-blue-50 to-white border-2 border-blue-200">
          <CardHeader>
            <CardTitle className="text-2xl">Building Coordination Infrastructure</CardTitle>
            <CardDescription className="text-base">
              What debtor nations need to coordinate effectively during restructuring negotiations
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="space-y-2">
                <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                  <Database className="h-5 w-5 text-blue-600" />
                </div>
                <h3 className="font-semibold text-slate-900">Precedent Database</h3>
                <p className="text-sm text-slate-600">
                  Searchable records of 500+ historical restructuring agreements showing terms, creditor compositions,
                  and documented outcomes for comparable cases.
                </p>
              </div>

              <div className="space-y-2">
                <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                  <BarChart className="h-5 w-5 text-blue-600" />
                </div>
                <h3 className="font-semibold text-slate-900">Analytical Tools</h3>
                <p className="text-sm text-slate-600">
                  Climate-adjusted debt sustainability analysis, scenario modeling, and fiscal space calculations using
                  IMF/World Bank frameworks with live data.
                </p>
              </div>

              <div className="space-y-2">
                <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                  <Users className="h-5 w-5 text-blue-600" />
                </div>
                <h3 className="font-semibold text-slate-900">Coordination Platform</h3>
                <p className="text-sm text-slate-600">
                  Secure communication channels, shared negotiation intelligence, and real-time coordination during
                  restructuring processes for collective strategy.
                </p>
              </div>
            </div>

            <div className="mt-6 p-4 bg-white rounded-lg border border-blue-200">
              <p className="text-sm text-slate-500">
                <strong className="text-slate-900">Current Status:</strong> Phase 1 infrastructure (precedent database,
                calculator, country profiles) is operational. Phase 2-4 analytical and coordination tools are under
                development as open-source projects.
              </p>
            </div>
          </CardContent>
        </Card>

        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-6">Tools & Data Available Now</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Card className="bg-white/80 backdrop-blur border-l-4 border-l-blue-500">
              <CardHeader>
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                    <BarChart className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <div className="inline-block px-2 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded mb-2">
                      Live Calculator
                    </div>
                    <CardTitle>Debt Relief Calculator</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-600 mb-4">
                  Model debt relief scenarios with live World Bank economic data showing fiscal space gains and social
                  investment opportunities.
                </p>
                <Link href="/calculator">
                  <Button variant="outline" className="w-full bg-transparent">
                    Calculate Scenarios
                  </Button>
                </Link>
              </CardContent>
            </Card>

            <Card className="bg-white/80 backdrop-blur border-l-4 border-l-blue-500">
              <CardHeader>
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                    <Search className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <div className="inline-block px-2 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded mb-2">
                      Live Database
                    </div>
                    <CardTitle>Precedents Database</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-600 mb-4">
                  29 verified restructuring cases (2005-2024) searchable by country, creditor type, and treatment
                  approach with documented outcomes.
                </p>
                <Link href="/precedents">
                  <Button variant="outline" className="w-full bg-transparent">
                    Search Precedents
                  </Button>
                </Link>
              </CardContent>
            </Card>

            <Card className="bg-white/80 backdrop-blur border-l-4 border-l-blue-500">
              <CardHeader>
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                    <Database className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <div className="inline-block px-2 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded mb-2">
                      Live Profiles
                    </div>
                    <CardTitle>Country Economic Profiles</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-600 mb-4">
                  16 country profiles with debt metrics, climate vulnerability data, and economic strengths from World
                  Bank and ND-GAIN sources.
                </p>
                <Link href="/countries">
                  <Button variant="outline" className="w-full bg-transparent">
                    View Countries
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>

        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-6">Research Library</h2>
          <p className="text-slate-600 mb-6">
            Policy frameworks, case studies, and legal templates supporting evidence-based debt coordination
          </p>
          <div className="grid md:grid-cols-2 gap-6">
            <Card className="bg-white/80 backdrop-blur border-l-4 border-l-slate-300 opacity-75">
              <CardHeader>
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-lg bg-slate-100 flex items-center justify-center flex-shrink-0">
                    <FileText className="h-6 w-6 text-slate-600" />
                  </div>
                  <div>
                    <div className="inline-block px-2 py-1 bg-slate-100 text-slate-600 text-xs font-semibold rounded mb-2">
                      Policy Brief
                    </div>
                    <CardTitle className="text-slate-700">Debt Sustainability Framework Reform</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-600 mb-4">
                  Analysis of current DSA models and proposals for climate-integrated alternatives that account for
                  vulnerability rather than just creditworthiness.
                </p>
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <AlertCircle className="h-4 w-4" />
                  <span>Coming Soon</span>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-white/80 backdrop-blur border-l-4 border-l-slate-300 opacity-75">
              <CardHeader>
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-lg bg-slate-100 flex items-center justify-center flex-shrink-0">
                    <BarChart className="h-6 w-6 text-slate-600" />
                  </div>
                  <div>
                    <div className="inline-block px-2 py-1 bg-slate-100 text-slate-600 text-xs font-semibold rounded mb-2">
                      Research Report
                    </div>
                    <CardTitle className="text-slate-700">The True Cost of Debt Service</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-600 mb-4">
                  Comprehensive analysis showing debt burdens crowd out health, education, and climate adaptation
                  spending across 60+ countries.
                </p>
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <AlertCircle className="h-4 w-4" />
                  <span>Coming Soon</span>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-white/80 backdrop-blur border-l-4 border-l-slate-300 opacity-75">
              <CardHeader>
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-lg bg-slate-100 flex items-center justify-center flex-shrink-0">
                    <BookOpen className="h-6 w-6 text-slate-600" />
                  </div>
                  <div>
                    <div className="inline-block px-2 py-1 bg-slate-100 text-slate-600 text-xs font-semibold rounded mb-2">
                      Case Study
                    </div>
                    <CardTitle className="text-slate-700">Debt-for-Climate Swap Mechanisms</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-600 mb-4">
                  Documentation of successful debt-relief linked to climate action in Belize, Seychelles, and Barbados,
                  showing replicable models.
                </p>
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <AlertCircle className="h-4 w-4" />
                  <span>Coming Soon</span>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-white/80 backdrop-blur border-l-4 border-l-slate-300 opacity-75">
              <CardHeader>
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-lg bg-slate-100 flex items-center justify-center flex-shrink-0">
                    <BookOpen className="h-6 w-6 text-slate-600" />
                  </div>
                  <div>
                    <div className="inline-block px-2 py-1 bg-slate-100 text-slate-600 text-xs font-semibold rounded mb-2">
                      Negotiation Toolkit
                    </div>
                    <CardTitle className="text-slate-700">Collective Coordination Guide</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-600 mb-4">
                  Strategies for aligning positions across debtor nations, building coalitions, and negotiating from
                  enhanced coordination.
                </p>
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <AlertCircle className="h-4 w-4" />
                  <span>Coming Soon</span>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-white/80 backdrop-blur border-l-4 border-l-slate-300 opacity-75">
              <CardHeader>
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-lg bg-slate-100 flex items-center justify-center flex-shrink-0">
                    <Scale className="h-6 w-6 text-slate-600" />
                  </div>
                  <div>
                    <div className="inline-block px-2 py-1 bg-slate-100 text-slate-600 text-xs font-semibold rounded mb-2">
                      Legal Framework
                    </div>
                    <CardTitle className="text-slate-700">Automatic Disaster Payment Pauses</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-600 mb-4">
                  Model provisions for climate disaster-triggered payment suspensions based on Barbados and Grenada
                  precedents.
                </p>
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <AlertCircle className="h-4 w-4" />
                  <span>Coming Soon</span>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-white/80 backdrop-blur border-l-4 border-l-slate-300 opacity-75">
              <CardHeader>
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-lg bg-slate-100 flex items-center justify-center flex-shrink-0">
                    <FileText className="h-6 w-6 text-slate-600" />
                  </div>
                  <div>
                    <div className="inline-block px-2 py-1 bg-slate-100 text-slate-600 text-xs font-semibold rounded mb-2">
                      Template Library
                    </div>
                    <CardTitle className="text-slate-700">Climate-Linked Debt Clause Examples</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-600 mb-4">
                  Collection of actual contract language from successful climate-linked debt restructurings for
                  adaptation.
                </p>
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <AlertCircle className="h-4 w-4" />
                  <span>Coming Soon</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-6">Development Roadmap</h2>
          <p className="text-slate-600 mb-6">
            Building open-source debt intelligence infrastructure for the global community
          </p>

          <div className="space-y-6">
            <Card className="bg-white border-l-4 border-l-blue-500">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <div className="inline-block px-2 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded mb-2">
                      Phase 1
                    </div>
                    <CardTitle>Enhanced Database</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-slate-600">
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    Expand to 50+ precedents from 1990-2024
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    Add bilateral restructuring cases (China, India, Saudi Arabia)
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5" />
                    Country economic strength indicators and sector analysis
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="bg-white border-l-4 border-l-teal-500">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <div className="inline-block px-2 py-1 bg-teal-100 text-teal-700 text-xs font-semibold rounded mb-2">
                      Phase 2
                    </div>
                    <CardTitle>Advanced Analytics Tools</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-slate-600">
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-teal-500 mt-1.5" />
                    Climate-Adjusted Debt Sustainability Analyzer
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-teal-500 mt-1.5" />
                    Multi-scenario comparison modeling
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-teal-500 mt-1.5" />
                    Debt-for-nature swap calculator
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-teal-500 mt-1.5" />
                    CBAM trade impact model
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="bg-white border-l-4 border-l-purple-500">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <div className="inline-block px-2 py-1 bg-purple-100 text-purple-700 text-xs font-semibold rounded mb-2">
                      Phase 3
                    </div>
                    <CardTitle>Research Library Expansion</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-slate-600">
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-purple-500 mt-1.5" />
                    Policy brief database
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-purple-500 mt-1.5" />
                    Legal framework templates
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-purple-500 mt-1.5" />
                    Negotiation strategy guides
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-purple-500 mt-1.5" />
                    Case study collection
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="bg-white border-l-4 border-l-amber-500">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <div className="inline-block px-2 py-1 bg-amber-100 text-amber-700 text-xs font-semibold rounded mb-2">
                      Phase 4
                    </div>
                    <CardTitle>API & Developer Tools</CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-slate-600">
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5" />
                    Public REST API for researchers
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5" />
                    Python/R statistical packages
                  </li>
                  <li className="flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5" />
                    Real-time debt monitor dashboard
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>

        <Card className="bg-gradient-to-br from-blue-50 to-white border-2 border-blue-200">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl mb-2">How to Contribute</CardTitle>
            <CardDescription>Help build debt intelligence infrastructure for the global community</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                  <GitBranch className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Submit Precedents</h3>
                  <p className="text-sm text-slate-600">
                    Contribute verified restructuring cases with source documentation via GitHub
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                  <Users className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Translate Tools</h3>
                  <p className="text-sm text-slate-600">Help reach French, Spanish, and Arabic-speaking officials</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                  <FileText className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Share Research</h3>
                  <p className="text-sm text-slate-600">Contribute anonymized country case studies and analysis</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                  <Code className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Develop Tools</h3>
                  <p className="text-sm text-slate-600">
                    Contribute to analytical tools and data visualization development
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-6 text-center">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white">
                <GitBranch className="mr-2 h-4 w-4" />
                View GitHub Repository
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="mt-8 bg-gradient-to-br from-slate-50 to-white border border-slate-200">
          <CardHeader className="text-center">
            <CardTitle className="text-xl mb-2">Data Sources</CardTitle>
            <CardDescription>All resources use verified data from official sources</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap justify-center gap-6 text-sm text-slate-600">
              <span>IMF Staff Reports</span>
              <span>•</span>
              <span>World Bank Publications</span>
              <span>•</span>
              <span>Paris Club Press Releases</span>
              <span>•</span>
              <span>UN Reports</span>
              <span>•</span>
              <span>Government Sources</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <Footer />
    </div>
  )
}
