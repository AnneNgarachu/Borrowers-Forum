"use client"

import { Badge } from "@/components/ui/badge"
import { EmptyState } from "@/components/ui/empty-state"
import { TrendingUp } from "lucide-react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { FileText, Search, Info, RefreshCw, X, Database, Globe, Calendar, Leaf } from "lucide-react"
import { searchPrecedentsAction } from "@/lib/api-actions"
import { historicalPrecedents } from "@/lib/precedents-data"
import { cn } from "@/lib/utils"
import type { Precedent } from "@/lib/api-actions"

export function PrecedentsSearch() {
  const [selectedCountry, setSelectedCountry] = useState<string>("all")
  const [selectedYearRange, setSelectedYearRange] = useState<string>("all")
  const [selectedCreditorType, setSelectedCreditorType] = useState<string>("all")
  const [selectedTreatmentType, setSelectedTreatmentType] = useState<string>("all")
  const [selectedClimateClause, setSelectedClimateClause] = useState<string>("all")
  const [selectedCreditor, setSelectedCreditor] = useState<string | null>(null)
  const [selectedRegion, setSelectedRegion] = useState<string | null>(null)
  const [expandedId, setExpandedId] = useState<string | null>(null)
  const [selectedPrecedent, setSelectedPrecedent] = useState<Precedent | null>(null)
  const [isDetailsOpen, setIsDetailsOpen] = useState(false)

  const [precedents, setPrecedents] = useState<Precedent[]>([])
  const [similarPrecedents, setSimilarPrecedents] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isFindingSimilar, setIsFindingSimilar] = useState(false)
  const [showSimilar, setShowSimilar] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [similarCountry, setSimilarCountry] = useState("GHA")
  const [similarAmount, setSimilarAmount] = useState("2000")
  const [usingFallbackData, setUsingFallbackData] = useState(false)

  useEffect(() => {
    loadPrecedents()
  }, [])

  const loadPrecedents = async () => {
    try {
      console.log("[v0] Loading precedents from API...")
      setIsLoading(true)
      setError(null)
      const data = await searchPrecedentsAction()

      console.log("[v0] Precedents loaded:", data?.length || 0, "cases")

      if (Array.isArray(data) && data.length > 0) {
        setPrecedents(data)
        setUsingFallbackData(false)
      } else {
        console.log("[v0] Using fallback historical precedents")
        setPrecedents(historicalPrecedents)
        setUsingFallbackData(true)
        setError("Using factual historical data. Connect API for live database access.")
      }
    } catch (err) {
      console.error("[v0] Error loading precedents:", err)
      setPrecedents(historicalPrecedents)
      setUsingFallbackData(true)
      setError("API unavailable. Showing factual historical precedents from our research database.")
    } finally {
      setIsLoading(false)
    }
  }

  const calculateSimilarity = (baseCase: any, compareCase: any): number => {
    if (baseCase.id === compareCase.id) return 0 // Don't compare to itself

    let score = 0

    // Region match (40 points)
    if (baseCase.country.region === compareCase.country.region) score += 40

    // Creditor type similarity (25 points)
    if (baseCase.creditor_type === compareCase.creditor_type) score += 25

    // Treatment type similarity (20 points)
    if (baseCase.treatment_type === compareCase.treatment_type) score += 20

    // Climate clause similarity (15 points)
    if (baseCase.includes_climate_clause === compareCase.includes_climate_clause) score += 15

    return score
  }

  const filteredPrecedents = precedents.filter((p) => {
    // When a specific country is selected, show ALL countries (we'll sort by similarity later)
    // When "all" is selected, apply normal filters
    const matchesCountry = selectedCountry === "all" || true // Always pass country filter when specific country selected

    const matchesCreditorType =
      selectedCreditorType === "all" || p.creditor_type.toLowerCase().includes(selectedCreditorType.toLowerCase())

    const matchesTreatmentType = selectedTreatmentType === "all" || p.treatment_type === selectedTreatmentType

    const matchesClimateClause = selectedClimateClause === "all" || p.includes_climate_clause === selectedClimateClause

    let matchesYear = true
    if (selectedYearRange !== "all") {
      if (selectedYearRange === "2020-2024") matchesYear = p.year >= 2020 && p.year <= 2024
      else if (selectedYearRange === "2015-2019") matchesYear = p.year >= 2015 && p.year <= 2019
      else if (selectedYearRange === "2010-2014") matchesYear = p.year >= 2010 && p.year <= 2014
      else if (selectedYearRange === "2005-2009") matchesYear = p.year >= 2005 && p.year <= 2009
    }

    const matchesCreditor = !selectedCreditor || p.creditor_type === selectedCreditor
    const matchesRegion = !selectedRegion || p.country.region === selectedRegion

    return (
      matchesCountry &&
      matchesCreditorType &&
      matchesTreatmentType &&
      matchesClimateClause &&
      matchesYear &&
      matchesCreditor &&
      matchesRegion
    )
  })

  const sortedPrecedents =
    selectedCountry !== "all"
      ? (() => {
          const baseCase = precedents.find((p) => p.country.name === selectedCountry)
          if (!baseCase) return filteredPrecedents

          // Get similar cases (excluding the base case itself)
          const similarCases = filteredPrecedents
            .map((p) => ({
              precedent: p,
              similarity: calculateSimilarity(baseCase, p),
            }))
            .filter((item) => item.precedent.id !== baseCase.id && item.similarity >= 60) // Exclude selected country and keep only 60%+
            .sort((a, b) => b.similarity - a.similarity) // Sort highest to lowest
            .map((item) => item.precedent)

          // Return selected country first, then similar cases
          return [baseCase, ...similarCases]
        })()
      : filteredPrecedents

  useEffect(() => {
    console.log("[v0] Search filters applied:", {
      selectedCountry,
      selectedYearRange,
      selectedCreditorType,
      selectedTreatmentType,
      selectedClimateClause,
      selectedCreditor,
      selectedRegion,
      totalPrecedents: precedents.length,
      filteredResults: filteredPrecedents.length,
    })
  }, [
    selectedCountry,
    selectedYearRange,
    selectedCreditorType,
    selectedTreatmentType,
    selectedClimateClause,
    selectedCreditor,
    selectedRegion,
    precedents.length,
    filteredPrecedents.length,
  ])

  const handleFindSimilar = async () => {
    try {
      setIsFindingSimilar(true)
      setError(null)
      const result = await fetch(
        `/api/similar-precedents?country_code=${similarCountry}&debt_amount_millions=${similarAmount}`,
      ).then((response) => response.json())
      setSimilarPrecedents(Array.isArray(result.similar_precedents) ? result.similar_precedents : [])
      setShowSimilar(true)
    } catch (err) {
      console.error("[v0] Error finding similar precedents:", err)
      setError(
        err instanceof Error ? err.message : "Failed to find similar precedents. Please check your API configuration.",
      )
      setSimilarPrecedents([])
    } finally {
      setIsFindingSimilar(false)
    }
  }

  const clearFilters = () => {
    setSelectedCountry("all")
    setSelectedYearRange("all")
    setSelectedCreditorType("all")
    setSelectedTreatmentType("all")
    setSelectedClimateClause("all")
    setSelectedCreditor(null)
    setSelectedRegion(null)
  }

  const getFlag = (code: string) => {
    const flags: Record<string, string> = {
      GHA: "🇬🇭",
      KEN: "🇰🇪",
      ZMB: "🇿🇲",
      BGD: "🇧🇩",
      ETH: "🇪🇹",
      TCD: "🇹🇩",
      ARG: "🇦🇷",
      LKA: "🇱🇰",
      ECU: "🇪🇨",
      SUR: "🇸🇷",
      UKR: "🇺🇦",
      LBN: "🇱🇧",
      MOZ: "🇲🇿",
      SEN: "🇸🇳",
    }
    return flags[code] || "🌍"
  }

  const openDetails = (precedent: Precedent) => {
    setSelectedPrecedent(precedent)
    setIsDetailsOpen(true)
  }

  const similarMatches = selectedCountry !== "all" ? sortedPrecedents.slice(1) : []

  return (
    <div className="space-y-6">
      <Card className="border-border/50 shadow-lg">
        <CardHeader className="bg-gradient-to-br from-[#1e3a5f]/5 to-transparent">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 flex-1">
              <div className="p-2 rounded-lg bg-[#1e3a5f] text-white">
                <FileText className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <CardTitle className="text-2xl">Precedent Intelligence Database</CardTitle>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger>
                        <Info className="h-4 w-4 text-muted-foreground" />
                      </TooltipTrigger>
                      <TooltipContent className="max-w-sm">
                        <p>
                          Search historical debt restructuring cases to find comparable agreements and understand what
                          terms similar nations achieved
                        </p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
                <CardDescription className="mt-1">
                  Search verified debt restructuring agreements from Paris Club, IMF HIPC Documents, and World Bank
                  sources (2005-2024)
                </CardDescription>
              </div>
            </div>
            <Button onClick={loadPrecedents} variant="outline" size="sm" disabled={isLoading}>
              <RefreshCw className={cn("h-4 w-4 mr-2", isLoading && "animate-spin")} />
              Refresh
            </Button>
          </div>
        </CardHeader>

        {/* Stats Banner */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 px-6 py-4 bg-slate-50 border-y border-slate-200">
          <Card className="p-4 bg-slate-50">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Database className="h-5 w-5 text-[#1e3a5f]" />
              </div>
              <div>
                <div className="text-2xl font-bold text-[#1e3a5f]">29</div>
                <div className="text-sm text-muted-foreground">Verified Precedents</div>
              </div>
            </div>
          </Card>

          <Card className="p-4 bg-slate-50">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Globe className="h-5 w-5 text-[#1e3a5f]" />
              </div>
              <div>
                <div className="text-2xl font-bold text-[#1e3a5f]">17</div>
                <div className="text-sm text-muted-foreground">Countries Covered</div>
              </div>
            </div>
          </Card>

          <Card className="p-4 bg-slate-50">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Calendar className="h-5 w-5 text-[#1e3a5f]" />
              </div>
              <div>
                <div className="text-2xl font-bold text-[#1e3a5f]">2005-2024</div>
                <div className="text-sm text-muted-foreground">Year Range</div>
              </div>
            </div>
          </Card>

          <Card className="p-4 bg-slate-50">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <Leaf className="h-5 w-5 text-green-700" />
              </div>
              <div>
                <div className="text-2xl font-bold text-green-700">12</div>
                <div className="text-sm text-muted-foreground">Climate-Linked</div>
              </div>
            </div>
          </Card>
        </div>

        <div className="px-6 py-2 bg-blue-50 border-b border-blue-100">
          <p className="text-xs text-slate-600 flex items-center gap-2">
            <Info className="h-3 w-3" />
            <span>
              Data sources: Paris Club Official Reports, IMF HIPC Documents, World Bank Debt Reports (2005-2024)
            </span>
          </p>
        </div>

        <CardContent className="pt-6 space-y-4">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            <Select value={selectedCountry} onValueChange={setSelectedCountry}>
              <SelectTrigger>
                <SelectValue placeholder="Country">
                  {selectedCountry === "all" ? "Country: All Countries" : `Country: ${selectedCountry}`}
                </SelectValue>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Countries</SelectItem>
                {[
                  "Argentina",
                  "Bangladesh",
                  "Belize",
                  "Chad",
                  "Ecuador",
                  "Ethiopia",
                  "Ghana",
                  "Grenada",
                  "Kenya",
                  "Lebanon",
                  "Madagascar",
                  "Malawi",
                  "Mozambique",
                  "Pakistan",
                  "São Tomé and Príncipe",
                  "Senegal",
                  "Sierra Leone",
                  "Somalia",
                  "Sri Lanka",
                  "Suriname",
                  "Ukraine",
                  "Zambia",
                ]
                  .sort()
                  .map((country) => (
                    <SelectItem key={country} value={country}>
                      {country}
                    </SelectItem>
                  ))}
              </SelectContent>
            </Select>

            <Select value={selectedYearRange} onValueChange={setSelectedYearRange}>
              <SelectTrigger>
                <SelectValue placeholder="Year Range">
                  {selectedYearRange === "all" ? "Year Range: All Years" : `Year Range: ${selectedYearRange}`}
                </SelectValue>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Years</SelectItem>
                <SelectItem value="2020-2024">2020-2024</SelectItem>
                <SelectItem value="2015-2019">2015-2019</SelectItem>
                <SelectItem value="2010-2014">2010-2014</SelectItem>
                <SelectItem value="2005-2009">2005-2009</SelectItem>
              </SelectContent>
            </Select>

            <Select value={selectedCreditorType} onValueChange={setSelectedCreditorType}>
              <SelectTrigger>
                <SelectValue placeholder="Creditor Type">
                  {selectedCreditorType === "all"
                    ? "Creditor Type: All"
                    : `Creditor Type: ${selectedCreditorType.charAt(0).toUpperCase() + selectedCreditorType.slice(1)}`}
                </SelectValue>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All</SelectItem>
                <SelectItem value="official">Official</SelectItem>
                <SelectItem value="private">Private</SelectItem>
                <SelectItem value="mixed">Mixed</SelectItem>
                <SelectItem value="paris club">Paris Club</SelectItem>
              </SelectContent>
            </Select>

            <Select value={selectedTreatmentType} onValueChange={setSelectedTreatmentType}>
              <SelectTrigger>
                <SelectValue placeholder="Treatment Type">
                  {selectedTreatmentType === "all" ? "Treatment Type: All" : `Treatment Type: ${selectedTreatmentType}`}
                </SelectValue>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All</SelectItem>
                <SelectItem value="Common Framework">Common Framework</SelectItem>
                <SelectItem value="Stock">Stock</SelectItem>
                <SelectItem value="Flow">Flow</SelectItem>
                <SelectItem value="DSSI">DSSI</SelectItem>
                <SelectItem value="Blue Bond">Debt-for-Nature</SelectItem>
                <SelectItem value="Default">Default</SelectItem>
                <SelectItem value="HIPC">HIPC</SelectItem>
              </SelectContent>
            </Select>

            <Select value={selectedClimateClause} onValueChange={setSelectedClimateClause}>
              <SelectTrigger>
                <SelectValue placeholder="Climate Clause">
                  {selectedClimateClause === "all" ? "Climate Clause: All" : `Climate Clause: ${selectedClimateClause}`}
                </SelectValue>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All</SelectItem>
                <SelectItem value="Yes">Yes</SelectItem>
                <SelectItem value="Partial">Partial</SelectItem>
                <SelectItem value="No">No</SelectItem>
              </SelectContent>
            </Select>

            <Button onClick={clearFilters} variant="outline" className="flex items-center gap-2 bg-transparent">
              <X className="h-4 w-4" />
              Clear Filters
            </Button>
          </div>

          <div className="flex flex-wrap gap-2">
            <Button
              variant={selectedCreditor === "Official" ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedCreditor(selectedCreditor === "Official" ? null : "Official")}
              className={cn(
                "rounded-full",
                selectedCreditor === "Official"
                  ? "bg-[#1e3a5f] hover:bg-[#1e3a5f]/90"
                  : "bg-transparent border-slate-300 hover:bg-slate-50",
              )}
            >
              ☑️ Official Creditors
            </Button>
            <Button
              variant={selectedCreditor === "Private" ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedCreditor(selectedCreditor === "Private" ? null : "Private")}
              className={cn(
                "rounded-full",
                selectedCreditor === "Private"
                  ? "bg-[#1e3a5f] hover:bg-[#1e3a5f]/90"
                  : "bg-transparent border-slate-300 hover:bg-slate-50",
              )}
            >
              ☐ Private Creditors
            </Button>
            <Button
              variant={selectedYearRange === "2020-2024" ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedYearRange(selectedYearRange === "2020-2024" ? "all" : "2020-2024")}
              className={cn(
                "rounded-full",
                selectedYearRange === "2020-2024"
                  ? "bg-[#1e3a5f] hover:bg-[#1e3a5f]/90"
                  : "bg-transparent border-slate-300 hover:bg-slate-50",
              )}
            >
              📅 Recent Cases (2020-2024)
            </Button>
            <Button
              variant={selectedTreatmentType === "Common Framework" ? "default" : "outline"}
              size="sm"
              onClick={() =>
                setSelectedTreatmentType(selectedTreatmentType === "Common Framework" ? "all" : "Common Framework")
              }
              className={cn(
                "rounded-full",
                selectedTreatmentType === "Common Framework"
                  ? "bg-[#1e3a5f] hover:bg-[#1e3a5f]/90"
                  : "bg-transparent border-slate-300 hover:bg-slate-50",
              )}
            >
              🤝 Common Framework
            </Button>
            <Button
              variant={selectedClimateClause === "Yes" ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedClimateClause(selectedClimateClause === "Yes" ? "all" : "Yes")}
              className={cn(
                "rounded-full",
                selectedClimateClause === "Yes"
                  ? "bg-[#1e3a5f] hover:bg-[#1e3a5f]/90"
                  : "bg-transparent border-slate-300 hover:bg-slate-50",
              )}
            >
              🌱 Climate-Linked
            </Button>
            <Button
              variant={selectedTreatmentType === "HIPC" ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedTreatmentType(selectedTreatmentType === "HIPC" ? "all" : "HIPC")}
              className={cn(
                "rounded-full",
                selectedTreatmentType === "HIPC"
                  ? "bg-[#1e3a5f] hover:bg-[#1e3a5f]/90"
                  : "bg-transparent border-slate-300 hover:bg-slate-50",
              )}
            >
              💼 HIPC Cases
            </Button>
            <Button
              variant={selectedCreditorType === "paris club" ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedCreditorType(selectedCreditorType === "paris club" ? "all" : "paris club")}
              className={cn(
                "rounded-full",
                selectedCreditorType === "paris club"
                  ? "bg-[#1e3a5f] hover:bg-[#1e3a5f]/90"
                  : "bg-transparent border-slate-300 hover:bg-slate-50",
              )}
            >
              🏛️ Paris Club
            </Button>
            <Button
              variant={selectedRegion === "South Asia" ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedRegion(selectedRegion === "South Asia" ? null : "South Asia")}
              className={cn(
                "rounded-full",
                selectedRegion === "South Asia"
                  ? "bg-[#1e3a5f] hover:bg-[#1e3a5f]/90"
                  : "bg-transparent border-slate-300 hover:bg-slate-50",
              )}
            >
              🌏 South Asia
            </Button>
            <Button
              variant={selectedTreatmentType === "Blue Bond" ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedTreatmentType(selectedTreatmentType === "Blue Bond" ? "all" : "Blue Bond")}
              className={cn(
                "rounded-full",
                selectedTreatmentType === "Blue Bond"
                  ? "bg-[#1e3a5f] hover:bg-[#1e3a5f]/90"
                  : "bg-transparent border-slate-300 hover:bg-slate-50",
              )}
            >
              🌊 Debt-for-Nature
            </Button>
          </div>

          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <span>
              Showing {sortedPrecedents.length} of {precedents.length} verified cases
            </span>
            {(selectedCountry !== "all" ||
              selectedYearRange !== "all" ||
              selectedCreditorType !== "all" ||
              selectedTreatmentType !== "all" ||
              selectedClimateClause !== "all" ||
              selectedCreditor ||
              selectedRegion) && (
              <Button onClick={clearFilters} variant="ghost" size="sm">
                Clear all filters
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {isLoading ? (
        <div className="py-12 text-center">
          <Search className="h-8 w-8 animate-spin mx-auto mb-3 text-[#1e3a5f]" />
          <p className="text-muted-foreground">Loading historical cases...</p>
        </div>
      ) : sortedPrecedents.length === 0 ? (
        <EmptyState
          title="No Results Found"
          description="Try adjusting your filters to see more precedents."
          icon={<FileText className="h-12 w-12" />}
        />
      ) : (
        <div className="grid lg:grid-cols-3 gap-6">
          {selectedCountry !== "all" ? (
            <>
              {/* Selected Country Card */}
              {sortedPrecedents.slice(0, 1).map((precedent) => (
                <Card key={precedent.id} className="hover:shadow-lg transition-shadow border-l-4 border-l-[#1e3a5f]">
                  <CardHeader className="pl-6">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <CardTitle className="text-lg flex items-center gap-2">
                          <span className="text-2xl">{getFlag(precedent.country.code)}</span>
                          {precedent.country.name}
                        </CardTitle>
                        <CardDescription className="text-xs mt-1">
                          {precedent.year} {precedent.treatment_type}
                        </CardDescription>
                      </div>
                    </div>
                  </CardHeader>

                  <CardContent className="space-y-3 pl-6">
                    <div className="text-sm space-y-2">
                      <div>
                        <span className="font-medium text-slate-600">Debt:</span>{" "}
                        <span className="font-semibold">${precedent.debt_amount_millions.toLocaleString()}M</span>{" "}
                        {precedent.treatment_type === "HIPC" ? "external" : "total"}
                      </div>
                      <div>
                        <span className="font-medium text-slate-600">Creditors:</span>{" "}
                        <span className="font-semibold">
                          {precedent.creditor_type === "Official"
                            ? "Official Creditor Committee"
                            : precedent.creditor_type}
                        </span>
                      </div>
                      <div>
                        <span className="font-medium text-slate-600">Source:</span>{" "}
                        <span className="text-xs text-slate-700">{precedent.source}</span>
                      </div>
                      {precedent.description && (
                        <div className="text-xs text-slate-600 leading-relaxed pt-2 border-t border-slate-100">
                          {precedent.description}
                        </div>
                      )}
                      <div>
                        <span className="font-medium text-slate-600">Status:</span>{" "}
                        <span className="text-slate-700">
                          {precedent.year >= 2022 ? "Active negotiations" : "Completed"}
                        </span>
                      </div>
                    </div>

                    <div className="pt-3 flex items-center gap-2">
                      <Badge variant="outline" className="text-xs">
                        <Globe className="h-3 w-3 mr-1" />
                        {precedent.country.region}
                      </Badge>
                    </div>

                    <Button
                      onClick={() => openDetails(precedent)}
                      variant="outline"
                      className="w-full mt-2 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white border-0 font-medium"
                    >
                      View Full Details →
                    </Button>
                  </CardContent>
                </Card>
              ))}

              {/* Similar Matches Section */}
              {selectedCountry !== "all" && similarMatches.length > 0 && (
                <div className="mt-8 mb-4">
                  <div className="flex items-center gap-3">
                    <h3 className="text-xl font-semibold text-[#1e3a5f]">Similar Matches</h3>
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <button className="text-slate-400 hover:text-slate-600">
                            <Info className="h-4 w-4" />
                          </button>
                        </TooltipTrigger>
                        <TooltipContent className="max-w-xs">
                          <p className="font-semibold mb-1">How Similarity is Calculated:</p>
                          <ul className="text-xs space-y-1">
                            <li>• Region Match: 40%</li>
                            <li>• Creditor Type: 25%</li>
                            <li>• Treatment Type: 20%</li>
                            <li>• Climate Clause: 15%</li>
                          </ul>
                          <p className="text-xs mt-2 text-muted-foreground">Only cases with 60%+ similarity shown</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                    <div className="flex-1 h-px bg-gradient-to-r from-[#1e3a5f] to-transparent ml-2"></div>
                  </div>
                </div>
              )}

              {sortedPrecedents.length > 1 && (
                <>
                  <div className="flex items-center gap-3 py-4">
                    <div className="h-px bg-gradient-to-r from-transparent via-slate-300 to-transparent flex-1" />
                    <div className="flex items-center gap-2 px-4 py-2 bg-amber-50 rounded-full border border-amber-200">
                      <TrendingUp className="h-4 w-4 text-amber-600" />
                      <span className="text-sm font-semibold text-amber-900">Similar Matches</span>
                      <Badge className="bg-amber-100 text-amber-700 border-amber-300 ml-1">
                        {similarMatches.length}
                      </Badge>
                    </div>
                    <div className="h-px bg-gradient-to-r from-transparent via-slate-300 to-transparent flex-1" />
                  </div>

                  {similarMatches.map((precedent) => {
                    const baseCase = precedents.find((p) => p.country.name === selectedCountry)
                    const similarity = baseCase ? calculateSimilarity(baseCase, precedent) : 0

                    return (
                      <Card
                        key={precedent.id}
                        className="hover:shadow-lg transition-shadow border-l-4 border-l-gradient-to-b from-[#1e3a5f] to-[#2d4a6f]"
                      >
                        <CardHeader className="pb-3">
                          <div className="flex items-start justify-between">
                            <div className="flex items-center gap-3">
                              <span className="text-3xl">{getFlag(precedent.country.code)}</span>
                              <div>
                                <CardTitle className="text-xl font-bold text-[#1e3a5f]">
                                  {precedent.country.code} {precedent.country.name}
                                </CardTitle>
                                <p className="text-sm text-slate-600 mt-1">
                                  {precedent.year} {precedent.treatment_type}
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-amber-50 to-yellow-50 rounded-lg border-2 border-amber-300 shadow-sm">
                              <TrendingUp className="h-4 w-4 text-amber-600" />
                              <span className="text-lg font-bold text-amber-900">{similarity}%</span>
                              <span className="text-xs text-amber-700 font-medium">Match</span>
                            </div>
                          </div>
                        </CardHeader>

                        <CardContent className="space-y-3 pl-6">
                          <div className="text-sm space-y-2">
                            <div>
                              <span className="font-medium text-slate-600">Debt:</span>{" "}
                              <span className="font-semibold">${precedent.debt_amount_millions.toLocaleString()}M</span>{" "}
                              {precedent.treatment_type === "HIPC" ? "external" : "total"}
                            </div>
                            <div>
                              <span className="font-medium text-slate-600">Creditors:</span>{" "}
                              <span className="font-semibold">
                                {precedent.creditor_type === "Official"
                                  ? "Official Creditor Committee"
                                  : precedent.creditor_type}
                              </span>
                            </div>
                            <div>
                              <span className="font-medium text-slate-600">Source:</span>{" "}
                              <span className="text-xs text-slate-700">{precedent.source}</span>
                            </div>
                            {precedent.description && (
                              <div className="text-xs text-slate-600 leading-relaxed pt-2 border-t border-slate-100">
                                {precedent.description}
                              </div>
                            )}
                            <div>
                              <span className="font-medium text-slate-600">Status:</span>{" "}
                              <span className="text-slate-700">
                                {precedent.year >= 2022 ? "Active negotiations" : "Completed"}
                              </span>
                            </div>
                          </div>

                          <div className="pt-3 flex items-center gap-2">
                            <Badge variant="outline" className="text-xs">
                              <Globe className="h-3 w-3 mr-1" />
                              {precedent.country.region}
                            </Badge>
                          </div>

                          <Button
                            onClick={() => openDetails(precedent)}
                            variant="outline"
                            className="w-full mt-2 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white border-0 font-medium"
                          >
                            View Full Details →
                          </Button>
                        </CardContent>
                      </Card>
                    )
                  })}
                </>
              )}
            </>
          ) : (
            // All countries view (no selection)
            sortedPrecedents.map((precedent) => (
              <Card
                key={precedent.id}
                className="hover:shadow-lg transition-shadow border-l-4 border-l-gradient-to-b from-[#1e3a5f] to-[#2d4a6f]"
              >
                <CardHeader className="pl-6">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <CardTitle className="text-lg flex items-center gap-2">
                        <span className="text-2xl">{getFlag(precedent.country.code)}</span>
                        {precedent.country.name}
                      </CardTitle>
                      <CardDescription className="text-xs mt-1">
                        {precedent.year} {precedent.treatment_type}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>

                <CardContent className="space-y-3 pl-6">
                  <div className="text-sm space-y-2">
                    <div>
                      <span className="font-medium text-slate-600">Debt:</span>{" "}
                      <span className="font-semibold">${precedent.debt_amount_millions.toLocaleString()}M</span>{" "}
                      {precedent.treatment_type === "HIPC" ? "external" : "total"}
                    </div>
                    <div>
                      <span className="font-medium text-slate-600">Creditors:</span>{" "}
                      <span className="font-semibold">
                        {precedent.creditor_type === "Official"
                          ? "Official Creditor Committee"
                          : precedent.creditor_type}
                      </span>
                    </div>
                    <div>
                      <span className="font-medium text-slate-600">Source:</span>{" "}
                      <span className="text-xs text-slate-700">{precedent.source}</span>
                    </div>
                    {precedent.description && (
                      <div className="text-xs text-slate-600 leading-relaxed pt-2 border-t border-slate-100">
                        {precedent.description}
                      </div>
                    )}
                    <div>
                      <span className="font-medium text-slate-600">Status:</span>{" "}
                      <span className="text-slate-700">
                        {precedent.year >= 2022 ? "Active negotiations" : "Completed"}
                      </span>
                    </div>
                  </div>

                  <div className="pt-3 flex items-center gap-2">
                    <Badge variant="outline" className="text-xs">
                      <Globe className="h-3 w-3 mr-1" />
                      {precedent.country.region}
                    </Badge>
                  </div>

                  <Button
                    onClick={() => openDetails(precedent)}
                    variant="outline"
                    className="w-full mt-2 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white border-0 font-medium"
                  >
                    View Full Details →
                  </Button>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      )}

      <Dialog open={isDetailsOpen} onOpenChange={setIsDetailsOpen}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          {selectedPrecedent && (
            <>
              <DialogHeader>
                <DialogTitle className="flex items-center gap-3 text-2xl">
                  <span className="text-3xl">{getFlag(selectedPrecedent.country.code)}</span>
                  {selectedPrecedent.country.name} - {selectedPrecedent.year}
                </DialogTitle>
                <DialogDescription>{selectedPrecedent.treatment_type} Restructuring Agreement</DialogDescription>
              </DialogHeader>

              <div className="space-y-6 pt-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <p className="text-sm font-medium text-slate-600">Total Debt Amount</p>
                    <p className="text-2xl font-bold text-[#1e3a5f]">
                      ${selectedPrecedent.debt_amount_millions.toLocaleString()}M
                    </p>
                  </div>
                  <div>
                    <div className="flex items-center gap-1 text-sm text-muted-foreground mb-1">
                      <span>NPV Reduction</span>
                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <button className="text-slate-400 hover:text-slate-600">
                              <Info className="h-3 w-3" />
                            </button>
                          </TooltipTrigger>
                          <TooltipContent className="max-w-xs">
                            <p className="text-xs">
                              Net Present Value reduction represents the actual debt relief value after discounting
                              future payments to today's value
                            </p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>
                    </div>
                    <p className="font-semibold">{selectedPrecedent.npv_reduction || "N/A"}</p>
                  </div>
                </div>

                <div className="space-y-3 border-t pt-4">
                  <div>
                    <p className="text-sm font-medium text-slate-600 mb-1">Creditor Type</p>
                    <Badge variant="outline" className="text-sm">
                      {selectedPrecedent.creditor_type}
                    </Badge>
                  </div>

                  <div>
                    <div className="flex items-center gap-1 text-sm text-muted-foreground mb-1">
                      <span>Treatment Type</span>
                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <button className="text-slate-400 hover:text-slate-600">
                              <Info className="h-3 w-3" />
                            </button>
                          </TooltipTrigger>
                          <TooltipContent className="max-w-xs">
                            <p className="text-xs font-semibold mb-1">Treatment Types:</p>
                            <ul className="text-xs space-y-1">
                              <li>
                                • <strong>Flow:</strong> Reschedules debt service payments
                              </li>
                              <li>
                                • <strong>Stock:</strong> Reduces total debt amount
                              </li>
                              <li>
                                • <strong>HIPC:</strong> Heavily Indebted Poor Countries relief
                              </li>
                              <li>
                                • <strong>Common Framework:</strong> G20 coordinated approach
                              </li>
                            </ul>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>
                    </div>
                    <Badge variant="outline">{selectedPrecedent.treatment_type}</Badge>
                  </div>

                  <div>
                    <p className="text-sm font-medium text-slate-600 mb-1">Climate Clause</p>
                    <Badge
                      variant="outline"
                      className={cn(
                        "text-sm",
                        selectedPrecedent.includes_climate_clause === "Yes" &&
                          "bg-green-100 text-green-800 border-green-300",
                        selectedPrecedent.includes_climate_clause === "Partial" &&
                          "bg-yellow-100 text-yellow-800 border-yellow-300",
                        selectedPrecedent.includes_climate_clause === "No" &&
                          "bg-gray-100 text-gray-600 border-gray-300",
                      )}
                    >
                      {selectedPrecedent.includes_climate_clause}
                    </Badge>
                  </div>

                  <div>
                    <p className="text-sm font-medium text-slate-600 mb-1">Region</p>
                    <p className="text-sm text-slate-700">{selectedPrecedent.country.region}</p>
                  </div>

                  <div>
                    <p className="text-sm font-medium text-slate-600 mb-1">Source</p>
                    <p className="text-sm text-slate-700">{selectedPrecedent.source}</p>
                  </div>

                  <div>
                    <p className="text-sm font-medium text-slate-600 mb-1">Last Updated</p>
                    <p className="text-sm text-slate-700">{selectedPrecedent.last_updated}</p>
                  </div>
                </div>

                <div className="border-t pt-4">
                  <p className="text-sm font-medium text-slate-600 mb-2">Description</p>
                  <p className="text-sm text-slate-700 leading-relaxed">{selectedPrecedent.description}</p>
                </div>

                <div className="border-t pt-4">
                  <p className="text-sm font-medium text-slate-600 mb-3">Similar Cases</p>
                  <div className="space-y-2">
                    {precedents
                      .filter((p) => p.id !== selectedPrecedent.id)
                      .map((p) => ({ case: p, similarity: calculateSimilarity(selectedPrecedent, p) }))
                      .filter((item) => item.similarity >= 60)
                      .sort((a, b) => b.similarity - a.similarity)
                      .slice(0, 3)
                      .map(({ case: similarCase, similarity }) => (
                        <div
                          key={similarCase.id}
                          className="p-3 bg-slate-50 rounded-lg border border-slate-200 hover:border-[#1e3a5f] transition-colors cursor-pointer"
                          onClick={() => {
                            setSelectedPrecedent(similarCase)
                          }}
                        >
                          <div className="flex items-center justify-between mb-1">
                            <div className="flex items-center gap-2">
                              <span className="text-lg">{getFlag(similarCase.country.code)}</span>
                              <span className="font-medium text-sm">{similarCase.country.name}</span>
                              <span className="text-xs text-slate-500">({similarCase.year})</span>
                            </div>
                            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200 text-xs">
                              {similarity}% match
                            </Badge>
                          </div>
                          <p className="text-xs text-slate-600">
                            ${similarCase.debt_amount_millions.toLocaleString()}M • {similarCase.treatment_type}
                          </p>
                          <p className="text-xs text-slate-600">Source: {similarCase.source}</p>
                        </div>
                      ))}
                  </div>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}
