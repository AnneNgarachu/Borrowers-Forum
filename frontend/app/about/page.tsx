import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { Breadcrumbs } from "@/components/breadcrumbs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Database,
  BarChart,
  Users,
  Shield,
  Globe,
  FileText,
} from "lucide-react"

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <Header />

      <div className="container mx-auto px-4 py-12 max-w-6xl">
        <Breadcrumbs />

        <div className="mb-12 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            About{" "}
            <span className="bg-gradient-to-r from-[#1e3a5f] to-[#2d5a8e] bg-clip-text text-transparent">
              The Platform
            </span>
          </h1>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto">
            Operationalizing digital infrastructure called for by the UN Expert Group on Debt
          </p>
        </div>

        {/* The Problem */}
        <Card className="mb-8 bg-gradient-to-br from-[#1e3a5f]/5 to-white border-2 border-[#1e3a5f]/15">
          <CardHeader>
            <CardTitle className="text-2xl text-[#1e3a5f]">The Information Asymmetry</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-slate-700 leading-relaxed">
              When countries need to restructure their debt, they often negotiate alone&mdash;without data on what terms
              other countries achieved or tools to analyze their options. Meanwhile, the institutions they negotiate with
              have had coordinated systems and shared intelligence since 1956.
            </p>
            <p className="text-slate-700 leading-relaxed font-medium">
              This platform helps level that playing field.
            </p>
          </CardContent>
        </Card>

        {/* What the Platform Provides */}
        <Card className="mb-8 bg-white border border-slate-200">
          <CardHeader>
            <CardTitle className="text-2xl">What We Provide</CardTitle>
            <CardDescription className="text-base">
              Three core capabilities for debt negotiation support
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="space-y-3">
                <div className="w-10 h-10 rounded-lg gradient-navy flex items-center justify-center">
                  <Database className="h-5 w-5 text-white" />
                </div>
                <h3 className="font-semibold text-slate-900">Precedent Database</h3>
                <p className="text-sm text-slate-600">
                  Searchable records of 20 verified historical restructuring agreements showing terms, creditor
                  compositions, and documented outcomes.
                </p>
              </div>

              <div className="space-y-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-teal-600 to-teal-500 flex items-center justify-center">
                  <BarChart className="h-5 w-5 text-white" />
                </div>
                <h3 className="font-semibold text-slate-900">Analytical Tools</h3>
                <p className="text-sm text-slate-600">
                  Debt relief impact calculator converting savings into healthcare, education, and climate
                  adaptation outcomes using verified economic data.
                </p>
              </div>

              <div className="space-y-3">
                <div className="w-10 h-10 rounded-lg gradient-gold flex items-center justify-center">
                  <Globe className="h-5 w-5 text-white" />
                </div>
                <h3 className="font-semibold text-slate-900">Country Profiles</h3>
                <p className="text-sm text-slate-600">
                  Economic and climate vulnerability profiles for 23 countries drawn from World Bank, IMF, and
                  ND-GAIN data sources.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Methodology & Data Sources */}
        <Card className="mb-8 bg-white border border-slate-200">
          <CardHeader>
            <CardTitle className="text-2xl">Methodology &amp; Data Sources</CardTitle>
            <CardDescription className="text-base">
              All data is compiled from official, publicly available sources
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="space-y-4">
                <h3 className="font-semibold text-slate-900 flex items-center gap-2">
                  <Shield className="h-4 w-4 text-[#1e3a5f]" />
                  Official Sources
                </h3>
                <ul className="space-y-3 text-sm text-slate-600">
                  <li className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#1e3a5f] mt-1.5 flex-shrink-0" />
                    <div>
                      <span className="font-medium text-slate-700">IMF Staff Reports &amp; Press Releases</span>
                      <p className="text-slate-500">Debt sustainability analyses, program documents, and lending data</p>
                    </div>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#1e3a5f] mt-1.5 flex-shrink-0" />
                    <div>
                      <span className="font-medium text-slate-700">Paris Club Official Reports</span>
                      <p className="text-slate-500">Agreed minutes and treatment terms for bilateral debt</p>
                    </div>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#1e3a5f] mt-1.5 flex-shrink-0" />
                    <div>
                      <span className="font-medium text-slate-700">World Bank WDI &amp; Debt Reports</span>
                      <p className="text-slate-500">Economic indicators, debt statistics, and development data</p>
                    </div>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#f59e0b] mt-1.5 flex-shrink-0" />
                    <div>
                      <span className="font-medium text-slate-700">ND-GAIN Climate Vulnerability Index</span>
                      <p className="text-slate-500">Country-level climate vulnerability and readiness scores</p>
                    </div>
                  </li>
                </ul>
              </div>

              <div className="space-y-4">
                <h3 className="font-semibold text-slate-900 flex items-center gap-2">
                  <FileText className="h-4 w-4 text-[#1e3a5f]" />
                  Coverage
                </h3>
                <ul className="space-y-3 text-sm text-slate-600">
                  <li className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#1e3a5f] mt-1.5 flex-shrink-0" />
                    <div>
                      <span className="font-medium text-slate-700">23 Countries</span>
                      <p className="text-slate-500">Sub-Saharan Africa, South Asia, Latin America &amp; Caribbean, MENA, Europe</p>
                    </div>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#1e3a5f] mt-1.5 flex-shrink-0" />
                    <div>
                      <span className="font-medium text-slate-700">20 Verified Precedents</span>
                      <p className="text-slate-500">HIPC, Common Framework, Paris Club, bilateral, and private restructurings</p>
                    </div>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#f59e0b] mt-1.5 flex-shrink-0" />
                    <div>
                      <span className="font-medium text-slate-700">12 Climate-Linked Cases</span>
                      <p className="text-slate-500">Including blue bonds, debt-for-nature swaps, and disaster clauses</p>
                    </div>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 rounded-full bg-teal-600 mt-1.5 flex-shrink-0" />
                    <div>
                      <span className="font-medium text-slate-700">5 Treatment Types</span>
                      <p className="text-slate-500">Flow, Stock, HIPC, Common Framework, Blue Bond</p>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Target Users */}
        <Card className="mb-8 bg-white border border-slate-200">
          <CardHeader>
            <CardTitle className="text-2xl">Built For</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="flex items-start gap-4 p-4 rounded-lg bg-slate-50">
                <div className="w-10 h-10 rounded-lg gradient-navy flex items-center justify-center flex-shrink-0">
                  <Users className="h-5 w-5 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Finance Ministers &amp; Debt Negotiators</h3>
                  <p className="text-sm text-slate-600">
                    Evidence-based analysis of restructuring options using verified precedents and live economic data
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4 p-4 rounded-lg bg-slate-50">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-teal-600 to-teal-500 flex items-center justify-center flex-shrink-0">
                  <BarChart className="h-5 w-5 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Policy Researchers &amp; Economists</h3>
                  <p className="text-sm text-slate-600">
                    Comprehensive debt-climate analysis with verified data from Paris Club, IMF, and World Bank
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Open Source */}
        <Card className="bg-gradient-to-br from-[#1e3a5f]/5 to-white border-2 border-[#1e3a5f]/15">
          <CardContent className="pt-6">
            <div className="text-center space-y-3">
              <p className="text-slate-700 font-medium">
                This platform is open source and built to be extended by the global development community.
              </p>
              <p className="text-sm text-slate-500">
                Conceptualized after the COP 30 Simulation Program. API documentation available for developers and researchers.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Footer />
    </div>
  )
}
