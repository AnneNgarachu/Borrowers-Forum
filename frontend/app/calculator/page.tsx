"use client"

import { DebtCalculator } from "@/components/debt-calculator"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { Breadcrumbs } from "@/components/breadcrumbs"

export default function CalculatorPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <Header />

      <div className="container mx-auto px-4 py-8">
        <Breadcrumbs />
        <DebtCalculator />
      </div>

      <Footer />
    </div>
  )
}
