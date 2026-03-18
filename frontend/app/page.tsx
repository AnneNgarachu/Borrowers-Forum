import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Calculator,
  Search,
  Globe,
  ArrowRight,
  Leaf,
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
            <span className="bg-gradient-to-r from-[#1e3a5f] to-[#2d5a8e] bg-clip-text text-transparent">
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
                className="gradient-navy hover:opacity-90 text-white shadow-lg shadow-[#1e3a5f]/30"
              >
                <Calculator className="mr-2 h-5 w-5" />
                Calculate Debt Impact
              </Button>
            </Link>
            <Link href="/precedents">
              <Button size="lg" variant="outline" className="border-2 border-[#1e3a5f]/20 hover:bg-[#1e3a5f]/5 bg-transparent text-[#1e3a5f]">
                <Search className="mr-2 h-5 w-5" />
                Explore Precedents
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 max-w-6xl mx-auto">
          <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-3xl font-bold text-[#1e3a5f]">
                23
              </CardTitle>
              <CardDescription className="text-slate-600">Countries Covered</CardDescription>
              <p className="text-xs text-slate-500 mt-1">Across 5 regions</p>
            </CardHeader>
          </Card>
          <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-3xl font-bold text-[#1e3a5f]">
                20
              </CardTitle>
              <CardDescription className="text-slate-600">Verified Cases</CardDescription>
              <p className="text-xs text-slate-500 mt-1">2018 &ndash; 2023 precedents</p>
            </CardHeader>
          </Card>
          <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-3xl font-bold text-[#b87a00]">
                12
              </CardTitle>
              <CardDescription className="text-slate-600">Climate-Linked</CardDescription>
              <p className="text-xs text-slate-500 mt-1">Debt + climate provisions</p>
            </CardHeader>
          </Card>
          <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm">
            <CardHeader className="pb-3">
              <CardTitle className="text-3xl font-bold text-[#1e3a5f]">
                $450B+
              </CardTitle>
              <CardDescription className="text-slate-600">Debt Restructured</CardDescription>
              <p className="text-xs text-slate-500 mt-1">Total across all cases</p>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* Features Grid - distinct colors per feature */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Platform Tools</h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Evidence-based tools for debt restructuring analysis
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Debt Calculator - Navy */}
            <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg gradient-navy flex items-center justify-center mb-4 shadow-lg shadow-[#1e3a5f]/30">
                  <Calculator className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-xl">Debt Relief Impact Calculator</CardTitle>
                <CardDescription className="text-slate-600">
                  Convert debt service savings into tangible outcomes
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-2 text-sm text-slate-600">
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-[#1e3a5f] mt-1.5" />
                  <span>Healthcare: Doctors employed for 1 or 5 years</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-[#1e3a5f] mt-1.5" />
                  <span>Education: Schools that could be built</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-[#1e3a5f] mt-1.5" />
                  <span>Climate: % of annual adaptation budget</span>
                </div>
                <Link href="/calculator">
                  <Button className="w-full mt-4 gradient-navy hover:opacity-90 text-white">
                    Start Calculating
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Precedents Search - Teal */}
            <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-teal-600 to-teal-500 flex items-center justify-center mb-4 shadow-lg shadow-teal-500/30">
                  <Search className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-xl">Verified Precedents</CardTitle>
                <CardDescription className="text-slate-600">Search 20 historical restructuring cases</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2 text-sm text-slate-600">
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-teal-600 mt-1.5" />
                  <span>Filter by creditor type, treatment, and year</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-teal-600 mt-1.5" />
                  <span>Similarity scoring to find comparable cases</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-teal-600 mt-1.5" />
                  <span>12 climate-linked restructuring cases</span>
                </div>
                <Link href="/precedents">
                  <Button className="w-full mt-4 bg-gradient-to-r from-teal-600 to-teal-500 hover:opacity-90 text-white">
                    Explore Precedents
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Country Profiles - Gold/Amber */}
            <Card className="bg-white/80 backdrop-blur border-slate-200 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg gradient-gold flex items-center justify-center mb-4 shadow-lg shadow-[#f59e0b]/30">
                  <Globe className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-xl">Country Profiles</CardTitle>
                <CardDescription className="text-slate-600">Economic and climate vulnerability data</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2 text-sm text-slate-600">
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-[#f59e0b] mt-1.5" />
                  <span>World Bank economic indicators</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-[#f59e0b] mt-1.5" />
                  <span>Climate vulnerability scoring (ND-GAIN)</span>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-[#f59e0b] mt-1.5" />
                  <span>23 debt-stressed countries covered</span>
                </div>
                <Link href="/countries">
                  <Button className="w-full mt-4 gradient-gold hover:opacity-90 text-white">
                    View Countries
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <Card className="gradient-navy border-0 text-white shadow-2xl shadow-[#1e3a5f]/30">
            <CardHeader className="text-center pb-6">
              <CardTitle className="text-3xl md:text-4xl font-bold mb-4">Ready to Explore Your Options?</CardTitle>
              <CardDescription className="text-slate-200 text-lg">
                Start analyzing debt relief scenarios and discover what your country could gain
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-wrap gap-4 justify-center">
              <Link href="/calculator">
                <Button size="lg" className="bg-white text-[#1e3a5f] hover:bg-slate-100 shadow-lg font-semibold">
                  <Calculator className="mr-2 h-5 w-5" />
                  Calculate Your Country's Potential
                </Button>
              </Link>
              <Link href="/countries">
                <Button
                  size="lg"
                  variant="outline"
                  className="border-2 border-white text-white hover:bg-white/10 bg-transparent"
                >
                  <Globe className="mr-2 h-5 w-5" />
                  View Country Profiles
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
