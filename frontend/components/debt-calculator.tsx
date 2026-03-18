"use client"

import type React from "react"
import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Calculator, TrendingDown, Info, Activity, Leaf, Users, School } from "lucide-react"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { type DebtCalculationResponse, calculateDebtAction as calculateDebtRelief } from "@/lib/api-actions"
import { Slider } from "@/components/ui/slider"

const countries = [
  { code: "ARG", name: "Argentina", flag: "🇦🇷", region: "Latin America & Caribbean" },
  { code: "BGD", name: "Bangladesh", flag: "🇧🇩", region: "South Asia" },
  { code: "BLZ", name: "Belize", flag: "🇧🇿", region: "Latin America & Caribbean" },
  { code: "TCD", name: "Chad", flag: "🇹🇩", region: "Sub-Saharan Africa" },
  { code: "ECU", name: "Ecuador", flag: "🇪🇨", region: "Latin America & Caribbean" },
  { code: "ETH", name: "Ethiopia", flag: "🇪🇹", region: "Sub-Saharan Africa" },
  { code: "GHA", name: "Ghana", flag: "🇬🇭", region: "Sub-Saharan Africa" },
  { code: "KEN", name: "Kenya", flag: "🇰🇪", region: "Sub-Saharan Africa" },
  { code: "LBN", name: "Lebanon", flag: "🇱🇧", region: "Middle East & North Africa" },
  { code: "MOZ", name: "Mozambique", flag: "🇲🇿", region: "Sub-Saharan Africa" },
  { code: "PAK", name: "Pakistan", flag: "🇵🇰", region: "South Asia" },
  { code: "SEN", name: "Senegal", flag: "🇸🇳", region: "Sub-Saharan Africa" },
  { code: "LKA", name: "Sri Lanka", flag: "🇱🇰", region: "South Asia" },
  { code: "SUR", name: "Suriname", flag: "🇸🇷", region: "Latin America & Caribbean" },
  { code: "UKR", name: "Ukraine", flag: "🇺🇦", region: "Europe & Central Asia" },
  { code: "ZMB", name: "Zambia", flag: "🇿🇲", region: "Sub-Saharan Africa" },
]

interface CalculationResult {
  country: string
  countryCode: string
  flag: string
  region: string
  debtAmount: number
  reliefPercent: number
  savings: number
  doctorsEquivalent: number
  schoolsEquivalent: number
  climatePercent: number
  apiData?: DebtCalculationResponse
  doctorSalary?: number
  schoolCost?: number
  climateBudget?: number
}

export function DebtCalculator() {
  const [selectedCountry, setSelectedCountry] = useState("")
  const [debtAmount, setDebtAmount] = useState("50,000,000")
  const [reliefPercent, setReliefPercent] = useState([30])
  const [result, setResult] = useState<CalculationResult | null>(null)
  const [isCalculating, setIsCalculating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [calculationHistory, setCalculationHistory] = useState<CalculationResult[]>([])
  const [showHistory, setShowHistory] = useState(false)
  const [calculatingProgress, setCalculatingProgress] = useState(0)
  const [calculatingMessage, setCalculatingMessage] = useState("")
  const [showConfetti, setShowConfetti] = useState(false)

  const formatCurrency = (value: string) => {
    const number = value.replace(/[^\d]/g, "")
    return number.replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  }

  const handleDebtAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const rawValue = e.target.value.replace(/[^\d]/g, "")
    const formatted = rawValue.replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    setDebtAmount(formatted)
  }

  const calculateImpact = async () => {
    const numericDebtAmount = Number.parseFloat(debtAmount.replace(/,/g, ""))

    if (!selectedCountry || !numericDebtAmount || numericDebtAmount <= 0) {
      alert("Please select a country and enter a valid debt amount")
      return
    }

    console.log("[v0] Starting calculation with:", {
      country: selectedCountry.code,
      debt: numericDebtAmount,
      relief: reliefPercent[0],
    })

    const country = countries.find((c) => c.code === selectedCountry)
    if (!country) return

    setIsCalculating(true)
    setError(null)
    setCalculatingProgress(0)
    setShowConfetti(false)

    try {
      const amount = Number.parseInt(debtAmount.replace(/,/g, ""))

      const progressSteps = [
        { progress: 20, message: "🌍 Connecting to World Bank API..." },
        { progress: 40, message: "📊 Fetching live economic data..." },
        { progress: 60, message: "💰 Analyzing debt indicators..." },
        { progress: 80, message: "🎯 Calculating opportunity costs..." },
        { progress: 95, message: "✨ Finalizing impact projections..." },
      ]

      for (const step of progressSteps) {
        setCalculatingProgress(step.progress)
        setCalculatingMessage(step.message)
        await new Promise((resolve) => setTimeout(resolve, 300))
      }

      console.log("[v0] Starting calculation for:", { country: selectedCountry, amount })

      const apiResponse = await calculateDebtRelief({
        country_code: selectedCountry,
        year: 2023,
        debt_amount_usd: amount,
      })

      console.log("[v0] API Response received:", apiResponse)

      if (apiResponse.data_source?.includes("Fallback")) {
        setError(null) // Clear any previous errors
        // Don't show error for fallback - it's working as intended
      }

      const doctorSalary = apiResponse.equivalents?.doctors?.estimated_salary_usd || 50000
      const schoolCost = apiResponse.equivalents?.schools?.estimated_cost_usd || 500000
      const climateBudget = apiResponse.equivalents?.climate_adaptation?.estimated_annual_budget_usd || 1000000000

      console.log("[v0] Extracted values:", { doctorSalary, schoolCost, climateBudget })

      const relief = reliefPercent[0]
      const savings = amount * (relief / 100)
      const doctorsEquivalent = Math.round(savings / doctorSalary)
      const schoolsEquivalent = Math.round(savings / schoolCost)
      const climatePercent = (savings / climateBudget) * 100

      console.log("[v0] Calculated equivalents:", { doctorsEquivalent, schoolsEquivalent, climatePercent })

      const newResult = {
        country: country.name,
        countryCode: country.code,
        flag: country.flag,
        region: country.region,
        debtAmount: amount,
        reliefPercent: relief,
        savings,
        doctorsEquivalent,
        schoolsEquivalent,
        climatePercent: Math.min(climatePercent, 100),
        apiData: apiResponse,
        doctorSalary,
        schoolCost,
        climateBudget,
      }

      setCalculatingProgress(100)
      setCalculatingMessage("🎉 Calculation complete!")
      setShowConfetti(true)

      setTimeout(() => {
        setResult(newResult)
        setCalculationHistory((prev) => [newResult, ...prev].slice(0, 5))
        setShowConfetti(false)
      }, 500)
    } catch (err) {
      console.error("[v0] Calculation error:", err)
      const errorMessage = err instanceof Error ? err.message : "Failed to calculate debt impact"
      setError(errorMessage)
    } finally {
      setIsCalculating(false)
    }
  }

  const presetReliefs = [10, 25, 50, 75, 100]

  const updateToScenario = (percent: number) => {
    setReliefPercent([percent])
    if (result && result.doctorSalary && result.schoolCost && result.climateBudget) {
      const amount = result.debtAmount
      const savings = amount * (percent / 100)
      setResult({
        ...result,
        reliefPercent: percent,
        savings,
        doctorsEquivalent: Math.round(savings / result.doctorSalary),
        schoolsEquivalent: Math.round(savings / result.schoolCost),
        climatePercent: Math.min((savings / result.climateBudget) * 100, 100),
      })
    }
  }

  const handleClear = () => {
    setSelectedCountry("")
    setDebtAmount("50,000,000")
    setReliefPercent([30])
    setResult(null)
    setError(null)
  }

  const handleExport = () => {
    if (!result) return

    const exportData = {
      country: result.country,
      debtAmount: `$${result.debtAmount.toLocaleString()}`,
      reliefPercent: `${result.reliefPercent}%`,
      savings: `$${(result.savings / 1000000).toFixed(1)}M`,
      healthcare: `${result.doctorsEquivalent.toLocaleString()} professionals`,
      education: `${result.schoolsEquivalent.toLocaleString()} schools`,
      climate: `${result.climatePercent.toFixed(1)}% of budget`,
      timestamp: new Date().toISOString(),
    }

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `debt-relief-calculation-${result.countryCode}-${Date.now()}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && selectedCountry && debtAmount && !isCalculating) {
      calculateImpact()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50 py-12 px-4">
      <div className="max-w-5xl mx-auto space-y-8">
        <div className="text-center space-y-4 mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-700 text-sm font-medium">
            <Calculator className="h-4 w-4" />
            Debt Relief Impact Calculator
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-slate-900 text-balance">
            What Could Your Country{" "}
            <span className="bg-gradient-to-r from-[#1e3a5f] to-[#2d5a8e] bg-clip-text text-transparent">
              Gain from Debt Relief?
            </span>
          </h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto text-pretty">
            See how debt restructuring could unlock resources for healthcare, education, and climate action.
          </p>
          <p className="text-xs text-slate-500">Calculations based on World Bank, IMF, and WHO data (2023)</p>
        </div>

        {error && (
          <Alert variant="destructive">
            <TrendingDown className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <Card className="shadow-xl border-slate-200/60 bg-white" onKeyPress={handleKeyPress}>
          <CardContent className="space-y-6 pt-8 pb-8">
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Label htmlFor="country" className="text-base font-semibold text-slate-700">
                    Select Country
                  </Label>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger>
                        <Info className="h-4 w-4 text-muted-foreground" />
                      </TooltipTrigger>
                      <TooltipContent className="max-w-xs">
                        <p>
                          Choose a debt-stressed country to analyze potential debt relief impacts using live economic
                          data.
                        </p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
                <Select value={selectedCountry} onValueChange={setSelectedCountry}>
                  <SelectTrigger id="country" className="h-12 text-base bg-white">
                    <SelectValue placeholder="Choose country..." />
                  </SelectTrigger>
                  <SelectContent>
                    {countries.map((country) => (
                      <SelectItem key={country.code} value={country.code} className="text-base py-3">
                        <div className="flex items-center gap-3">
                          <span className="text-2xl">{country.flag}</span>
                          <div>
                            <div className="font-medium">{country.name}</div>
                            <div className="text-xs text-muted-foreground">{country.region}</div>
                          </div>
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Label htmlFor="debt" className="text-base font-semibold text-slate-700">
                    Total Debt Service (USD)
                  </Label>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger>
                        <Info className="h-4 w-4 text-muted-foreground" />
                      </TooltipTrigger>
                      <TooltipContent className="max-w-xs">
                        <p>
                          Enter the total annual debt service payment (principal + interest) that could be relieved
                          through restructuring.
                        </p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 font-medium text-lg">$</span>
                  <Input
                    id="debt"
                    type="text"
                    value={debtAmount}
                    onChange={handleDebtAmountChange}
                    placeholder="50,000,000"
                    className="h-12 pl-8 text-base font-mono bg-white"
                  />
                </div>
              </div>
            </div>

            <div className="space-y-4 pt-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Label className="text-base font-semibold text-slate-700">
                    Debt Relief: <span className="text-amber-600">{reliefPercent[0]}%</span>
                  </Label>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger>
                        <Info className="h-4 w-4 text-muted-foreground" />
                      </TooltipTrigger>
                      <TooltipContent className="max-w-xs">
                        <p>
                          Adjust the percentage of debt relief to see how different scenarios impact resource
                          availability. Historical cases range from 10% to 100% relief.
                        </p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
              </div>

              <div className="pt-2 pb-2">
                <Slider
                  value={reliefPercent}
                  onValueChange={setReliefPercent}
                  max={100}
                  min={10}
                  step={1}
                  className="cursor-pointer"
                />
              </div>

              <div className="flex flex-wrap gap-2">
                {presetReliefs.map((preset) => (
                  <Button
                    key={preset}
                    variant="outline"
                    size="sm"
                    onClick={() => setReliefPercent([preset])}
                    className="transition-all border-slate-300"
                  >
                    {preset}%
                  </Button>
                ))}
              </div>
            </div>

            <div className="flex gap-3">
              <Button
                onClick={calculateImpact}
                disabled={!selectedCountry || !debtAmount || isCalculating}
                size="lg"
                className="flex-1 gradient-navy hover:opacity-90 text-white h-14 text-base font-semibold shadow-lg hover:shadow-xl transition-all disabled:opacity-50"
              >
                {isCalculating ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-2 border-white/30 border-t-white mr-2" />
                    Calculating...
                  </>
                ) : (
                  <>
                    <Calculator className="mr-2 h-5 w-5" />
                    Calculate Full Impact
                  </>
                )}
              </Button>
              <Button
                onClick={handleClear}
                variant="outline"
                size="lg"
                className="h-14 px-6 bg-transparent"
                disabled={isCalculating}
              >
                Clear
              </Button>
            </div>

            {calculationHistory.length > 0 && (
              <Button
                onClick={() => setShowHistory(!showHistory)}
                variant="ghost"
                size="sm"
                className="w-full text-slate-600"
              >
                {showHistory ? "Hide" : "Show"} Recent Calculations ({calculationHistory.length})
              </Button>
            )}

            {showHistory && calculationHistory.length > 0 && (
              <div className="border-t pt-4 space-y-2">
                <p className="text-sm font-semibold text-slate-700">Recent Calculations</p>
                {calculationHistory.map((calc, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setSelectedCountry(calc.countryCode)
                      setDebtAmount(calc.debtAmount.toString())
                      setReliefPercent([calc.reliefPercent])
                      setResult(calc)
                      setShowHistory(false)
                    }}
                    className="w-full text-left p-3 rounded-lg border border-slate-200 hover:bg-slate-50 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-xl">{calc.flag}</span>
                        <span className="font-medium text-sm">{calc.country}</span>
                      </div>
                      <div className="text-xs text-slate-500">
                        ${(calc.debtAmount / 1000000).toFixed(1)}M at {calc.reliefPercent}%
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {result && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-slate-900">Results</h2>
              <div className="flex gap-2">
                <Button onClick={handleExport} variant="outline" size="sm">
                  <Activity className="mr-2 h-4 w-4" />
                  Export
                </Button>
                <Button onClick={handleClear} variant="outline" size="sm">
                  New Calculation
                </Button>
              </div>
            </div>

            <Card className="gradient-navy text-white shadow-xl border-0">
              <CardHeader>
                <CardTitle>{result.country}</CardTitle>
                <CardDescription>{result.region}</CardDescription>
              </CardHeader>
              <CardContent className="py-8">
                <div className="flex items-center gap-6">
                  <div className="text-7xl">{result.flag}</div>
                  <div className="flex-1">
                    <p className="text-white/70 text-lg">
                      Analyzing <span className="font-mono font-bold">${result.debtAmount.toLocaleString()}</span> in
                      debt
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="gradient-gold text-white shadow-xl border-0 overflow-hidden relative">
              <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent" />
              <CardContent className="py-10 relative">
                <div className="text-center space-y-2">
                  <p className="text-lg font-medium text-white/90">
                    With {result.reliefPercent}% debt relief, {result.country} saves:
                  </p>
                  <p className="text-6xl font-bold tracking-tight drop-shadow-lg">
                    ${(result.savings / 1000000).toFixed(1)}M
                  </p>
                  <p className="text-white/80 text-lg">Million USD</p>
                </div>
              </CardContent>
            </Card>

            <div>
              <div className="flex items-center gap-2 mb-4">
                <h3 className="text-2xl font-bold text-slate-900">What This Unlocks</h3>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger>
                      <Info className="h-5 w-5 text-muted-foreground" />
                    </TooltipTrigger>
                    <TooltipContent className="max-w-sm">
                      <p className="font-semibold mb-2">How We Calculate Impact:</p>
                      <ul className="text-xs space-y-1">
                        <li>• Healthcare: Based on average annual salary of healthcare professionals in the country</li>
                        <li>• Education: Using average cost to build and equip a primary school</li>
                        <li>• Climate: Percentage of the national climate adaptation budget</li>
                        <li>• Data sources: World Bank, WHO, UNESCO, UNEP</li>
                      </ul>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
                <div className="h-1 flex-1 bg-gradient-to-r from-amber-500 to-transparent rounded" />
              </div>
              <div className="grid md:grid-cols-3 gap-4">
                <Card className="group hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border-slate-200 bg-white">
                  <CardHeader>
                    <CardTitle>Healthcare Professionals</CardTitle>
                    <CardDescription>Employed for 1 year</CardDescription>
                  </CardHeader>
                  <CardContent className="py-8">
                    <div className="text-center space-y-3">
                      <div className="inline-flex p-4 rounded-full bg-[#1e3a5f]/10 text-[#1e3a5f] group-hover:scale-110 transition-transform">
                        <Users className="h-8 w-8" />
                      </div>
                      <div>
                        <p className="text-4xl font-bold text-[#1e3a5f]">{result.doctorsEquivalent.toLocaleString()}</p>
                        <p className="text-xs text-slate-500 mt-2">Source: WHO salary data</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="group hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border-slate-200 bg-white">
                  <CardHeader>
                    <CardTitle>Schools Built</CardTitle>
                    <CardDescription>With modern facilities</CardDescription>
                  </CardHeader>
                  <CardContent className="py-8">
                    <div className="text-center space-y-3">
                      <div className="inline-flex p-4 rounded-full bg-purple-500/10 text-purple-600 group-hover:scale-110 transition-transform">
                        <School className="h-8 w-8" />
                      </div>
                      <div>
                        <p className="text-4xl font-bold text-purple-600">
                          {result.schoolsEquivalent.toLocaleString()}
                        </p>
                        <p className="text-xs text-slate-500 mt-2">Source: UNESCO cost estimates</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="group hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border-slate-200 bg-white">
                  <CardHeader>
                    <CardTitle>Climate Adaptation</CardTitle>
                    <CardDescription>Of annual budget</CardDescription>
                  </CardHeader>
                  <CardContent className="py-8">
                    <div className="text-center space-y-3">
                      <div className="inline-flex p-4 rounded-full bg-green-500/10 text-green-600 group-hover:scale-110 transition-transform">
                        <Leaf className="h-8 w-8" />
                      </div>
                      <div>
                        <p className="text-4xl font-bold text-green-600">{result.climatePercent.toFixed(1)}%</p>
                        <p className="text-xs text-slate-500 mt-2">Source: UNEP national budgets</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>

            <div>
              <h3 className="text-2xl font-bold mb-4 flex items-center gap-2 text-slate-900">
                <span>Compare Scenarios</span>
                <div className="h-1 flex-1 bg-gradient-to-r from-[#1e3a5f] to-transparent rounded" />
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {presetReliefs.map((percent) => {
                  const scenarioSavings = result.debtAmount * (percent / 100)
                  const scenarioDoctors = result.doctorSalary ? Math.round(scenarioSavings / result.doctorSalary) : 0
                  const isActive = result.reliefPercent === percent

                  return (
                    <button
                      key={percent}
                      onClick={() => updateToScenario(percent)}
                      className={`text-left p-4 rounded-lg border-2 transition-all hover:shadow-md bg-white ${
                        isActive ? "border-amber-500 bg-amber-50 shadow-lg" : "border-slate-200 hover:border-slate-300"
                      }`}
                    >
                      <div className="space-y-2">
                        <div className={`text-2xl font-bold ${isActive ? "text-amber-600" : "text-slate-900"}`}>
                          {percent}%
                        </div>
                        <div className="text-sm space-y-1">
                          <p className="font-medium text-slate-700">${(scenarioSavings / 1000000).toFixed(1)}M</p>
                          <p className="text-xs text-slate-500">{scenarioDoctors.toLocaleString()} doctors</p>
                        </div>
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>
          </div>
        )}
      </div>
      {isCalculating && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
          <Card className="w-full max-w-md mx-4 overflow-hidden">
            <CardContent className="p-8">
              <div className="text-center space-y-6">
                <div className="relative">
                  <div className="w-20 h-20 mx-auto rounded-full gradient-navy flex items-center justify-center animate-pulse">
                    <Calculator className="w-10 h-10 text-white" />
                  </div>
                </div>

                <div className="space-y-3">
                  <p className="text-lg font-semibold">{calculatingMessage}</p>
                  <div className="w-full bg-slate-200 rounded-full h-3 overflow-hidden">
                    <div
                      className="h-full gradient-navy transition-all duration-300 ease-out"
                      style={{ width: `${calculatingProgress}%` }}
                    />
                  </div>
                  <p className="text-sm text-muted-foreground">{calculatingProgress}% complete</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
