"use client"

import { useState, useEffect } from "react"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { Breadcrumbs } from "@/components/breadcrumbs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Button } from "@/components/ui/button"
import { Users, DollarSign, AlertCircle, Loader2, Info, X, TrendingUp } from "lucide-react"
import { getAllCountriesAction, type Country } from "@/lib/api-actions"
import { COUNTRY_PROFILES, type CountryProfile } from "@/lib/countries-data"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { EmptyState } from "@/components/empty-state"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export default function CountriesPage() {
  const [countries, setCountries] = useState<(Country | CountryProfile)[]>(COUNTRY_PROFILES)
  const [filteredCountries, setFilteredCountries] = useState<(Country | CountryProfile)[]>(COUNTRY_PROFILES)
  const [selectedCountry, setSelectedCountry] = useState("all")
  const [selectedRegion, setSelectedRegion] = useState("all")
  const [selectedIncomeLevel, setSelectedIncomeLevel] = useState("all")
  const [isLoading, setIsLoading] = useState(false)
  const [usingFallbackData, setUsingFallbackData] = useState(true)

  useEffect(() => {
    loadCountries()
  }, [])

  useEffect(() => {
    console.log("[v0] Countries search filter applied:", {
      selectedCountry,
      selectedRegion,
      selectedIncomeLevel,
      totalCountries: countries.length,
      filteredResults: filteredCountries.length,
    })
  }, [selectedCountry, selectedRegion, selectedIncomeLevel, filteredCountries.length, countries.length])

  useEffect(() => {
    const countriesArray = Array.isArray(countries) ? countries : COUNTRY_PROFILES

    const filtered = countriesArray.filter((country) => {
      const matchesCountry = selectedCountry === "all" || country.name === selectedCountry
      const matchesRegion = selectedRegion === "all" || country.region === selectedRegion
      const matchesIncomeLevel = selectedIncomeLevel === "all" || country.income_level === selectedIncomeLevel

      return matchesCountry && matchesRegion && matchesIncomeLevel
    })

    setFilteredCountries(filtered)
  }, [selectedCountry, selectedRegion, selectedIncomeLevel, countries])

  const loadCountries = async () => {
    try {
      console.log("[v0] Loading countries from API...")
      setIsLoading(true)
      const data = await getAllCountriesAction()

      console.log("[v0] Countries loaded:", data?.length || 0, "countries")

      if (Array.isArray(data) && data.length > 0) {
        setCountries(data)
        setFilteredCountries(data)
        setUsingFallbackData(false)
      } else {
        console.log("[v0] Invalid data format from API, using factual preloaded data")
      }
    } catch (err) {
      console.log("[v0] API unavailable, using factual preloaded data from World Bank/IMF sources")
      setUsingFallbackData(true)
    } finally {
      setIsLoading(false)
    }
  }

  const clearFilters = () => {
    setSelectedCountry("all")
    setSelectedRegion("all")
    setSelectedIncomeLevel("all")
  }

  const hasActiveFilters = selectedCountry !== "all" || selectedRegion !== "all" || selectedIncomeLevel !== "all"

  const getFlag = (code: string) => {
    const flags: Record<string, string> = {
      GHA: "🇬🇭",
      KEN: "🇰🇪",
      ZMB: "🇿🇲",
      EGY: "🇪🇬",
      PAK: "🇵🇰",
      BGD: "🇧🇩",
      ETH: "🇪🇹",
      SEN: "🇸🇳",
      ARG: "🇦🇷",
      BLZ: "🇧🇿",
      TCD: "🇹🇩",
      ECU: "🇪🇨",
      LBN: "🇱🇧",
      MOZ: "🇲🇿",
      LKA: "🇱🇰",
      SUR: "🇸🇷",
      UKR: "🇺🇦",
    }
    return flags[code] || "🌍"
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <Header />

      <main className="container mx-auto px-4 py-8 space-y-6">
        <Breadcrumbs />

        <Card className="border-border/50 shadow-lg">
          <CardHeader className="bg-gradient-to-br from-[#1e3a5f]/5 to-transparent">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-[#1e3a5f] text-white">
                  <Users className="h-5 w-5" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <CardTitle className="text-2xl">Country Economic Profiles</CardTitle>
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger>
                          <Info className="h-4 w-4 text-muted-foreground" />
                        </TooltipTrigger>
                        <TooltipContent className="max-w-xs">
                          <p>
                            Economic indicators, debt metrics, and climate vulnerability data for countries with active
                            restructuring cases in our database
                          </p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  </div>
                  <CardDescription className="mt-1">
                    Economic indicators, debt metrics, and climate vulnerability data for 16 countries with active
                    restructuring cases
                  </CardDescription>
                </div>
              </div>
            </div>
          </CardHeader>

          <div className="px-6 py-2 bg-blue-50 border-t border-blue-100">
            <p className="text-xs text-slate-600 flex items-center gap-2">
              <Info className="h-3 w-3" />
              <span>Data sources: World Bank WDI, IMF WEO, ND-GAIN Climate Index (2023 data)</span>
            </p>
          </div>
        </Card>

        <Card className="border-border/50">
          <CardContent className="pt-6">
            <div className="flex flex-wrap gap-3 items-center">
              <Select value={selectedCountry} onValueChange={setSelectedCountry}>
                <SelectTrigger className="w-[200px]">
                  <SelectValue placeholder="All Countries" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Countries</SelectItem>
                  <SelectItem value="Argentina">Argentina</SelectItem>
                  <SelectItem value="Bangladesh">Bangladesh</SelectItem>
                  <SelectItem value="Belize">Belize</SelectItem>
                  <SelectItem value="Chad">Chad</SelectItem>
                  <SelectItem value="Ecuador">Ecuador</SelectItem>
                  <SelectItem value="Ethiopia">Ethiopia</SelectItem>
                  <SelectItem value="Ghana">Ghana</SelectItem>
                  <SelectItem value="Kenya">Kenya</SelectItem>
                  <SelectItem value="Lebanon">Lebanon</SelectItem>
                  <SelectItem value="Mozambique">Mozambique</SelectItem>
                  <SelectItem value="Pakistan">Pakistan</SelectItem>
                  <SelectItem value="Senegal">Senegal</SelectItem>
                  <SelectItem value="Sri Lanka">Sri Lanka</SelectItem>
                  <SelectItem value="Suriname">Suriname</SelectItem>
                  <SelectItem value="Ukraine">Ukraine</SelectItem>
                  <SelectItem value="Zambia">Zambia</SelectItem>
                </SelectContent>
              </Select>

              <Select value={selectedRegion} onValueChange={setSelectedRegion}>
                <SelectTrigger className="w-[220px]">
                  <SelectValue placeholder="All Regions" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Regions</SelectItem>
                  <SelectItem value="Sub-Saharan Africa">Sub-Saharan Africa</SelectItem>
                  <SelectItem value="South Asia">South Asia</SelectItem>
                  <SelectItem value="Latin America & Caribbean">Latin America & Caribbean</SelectItem>
                  <SelectItem value="Middle East & North Africa">Middle East & North Africa</SelectItem>
                  <SelectItem value="Europe & Central Asia">Europe & Central Asia</SelectItem>
                </SelectContent>
              </Select>

              <Select value={selectedIncomeLevel} onValueChange={setSelectedIncomeLevel}>
                <SelectTrigger className="w-[200px]">
                  <SelectValue placeholder="All Income Levels" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Income Levels</SelectItem>
                  <SelectItem value="Low Income">Low Income</SelectItem>
                  <SelectItem value="Lower-Middle Income">Lower-Middle Income</SelectItem>
                  <SelectItem value="Upper-Middle Income">Upper-Middle Income</SelectItem>
                </SelectContent>
              </Select>

              {hasActiveFilters && (
                <Button onClick={clearFilters} variant="outline" size="sm" className="gap-2 bg-transparent">
                  <X className="h-4 w-4" />
                  Clear Filters
                </Button>
              )}

              <Button
                onClick={loadCountries}
                variant="outline"
                size="sm"
                disabled={isLoading}
                className="ml-auto bg-transparent"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Refreshing...
                  </>
                ) : (
                  "Refresh Data"
                )}
              </Button>
            </div>
            <p className="text-xs text-muted-foreground mt-3 flex items-center gap-1.5">
              <Info className="h-3 w-3" />
              Showing countries with active debt restructuring cases in our database
            </p>
          </CardContent>
        </Card>

        {isLoading ? (
          <div className="py-12 text-center">
            <Loader2 className="h-8 w-8 animate-spin mx-auto mb-3 text-[#1e3a5f]" />
            <p className="text-muted-foreground">Loading country profiles...</p>
          </div>
        ) : filteredCountries.length === 0 ? (
          <EmptyState
            icon={Users}
            title="No countries found"
            description="No countries match your selected filters. Try adjusting your selection."
            action={
              <Button onClick={clearFilters} variant="outline">
                Clear Filters
              </Button>
            }
          />
        ) : (
          <>
            <div className="text-sm text-muted-foreground flex items-center justify-between">
              <span>
                Showing {filteredCountries.length} of {countries.length} countries
              </span>
              {hasActiveFilters && (
                <Button variant="ghost" size="sm" onClick={clearFilters}>
                  Clear filters
                </Button>
              )}
            </div>
            <div className="grid lg:grid-cols-2 gap-6">
              {filteredCountries.map((country) => (
                <Card key={country.code} className="border-border/50 hover:shadow-xl transition-all bg-white">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-4">
                        <span className="text-5xl">{getFlag(country.code)}</span>
                        <div>
                          <CardTitle className="text-xl">{country.name}</CardTitle>
                          <CardDescription className="mt-1">{country.region}</CardDescription>
                        </div>
                      </div>
                      <Badge variant="secondary" className="text-xs">
                        {country.income_level}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {"summary" in country && country.summary && (
                      <p className="text-sm text-slate-600 leading-relaxed">{country.summary}</p>
                    )}

                    {"key_sectors" in country && country.key_sectors && country.key_sectors.length > 0 && (
                      <div className="p-3 bg-blue-50/50 rounded-lg border border-blue-100">
                        <div className="flex items-start gap-2 mb-2">
                          <TrendingUp className="h-4 w-4 text-blue-600 mt-0.5" />
                          <div className="flex-1">
                            <p className="text-sm font-semibold text-slate-700">Key Economic Sectors</p>
                            <div className="flex flex-wrap gap-1.5 mt-1.5">
                              {country.key_sectors.map((sector) => (
                                <Badge key={sector} variant="secondary" className="text-xs bg-white">
                                  {sector}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        </div>
                        {country.gdp_growth_rate !== undefined && (
                          <div className="flex items-center gap-2 mt-2 text-sm">
                            <span className="text-slate-600">GDP Growth:</span>
                            <span
                              className={`font-semibold ${
                                country.gdp_growth_rate >= 0 ? "text-green-700" : "text-red-700"
                              }`}
                            >
                              {country.gdp_growth_rate > 0 ? "+" : ""}
                              {country.gdp_growth_rate.toFixed(1)}%
                            </span>
                            <span className="text-xs text-slate-500">(2023)</span>
                          </div>
                        )}
                      </div>
                    )}

                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <DollarSign className="h-3.5 w-3.5" />
                          <span>GDP</span>
                          <TooltipProvider>
                            <Tooltip>
                              <TooltipTrigger>
                                <Info className="h-3 w-3 text-muted-foreground/60" />
                              </TooltipTrigger>
                              <TooltipContent>
                                <p>Gross Domestic Product in USD billions</p>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        </div>
                        <p className="text-2xl font-bold">${country.gdp_usd_billions.toFixed(1)}B</p>
                      </div>
                      <div className="space-y-1">
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <Users className="h-3.5 w-3.5" />
                          <span>Population</span>
                        </div>
                        <p className="text-2xl font-bold">{(country.population / 1000000).toFixed(1)}M</p>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-2">
                          <AlertCircle className="h-3.5 w-3.5 text-muted-foreground" />
                          <span className="font-medium">Climate Vulnerability Score</span>
                          <TooltipProvider>
                            <Tooltip>
                              <TooltipTrigger>
                                <Info className="h-3 w-3 text-muted-foreground/60" />
                              </TooltipTrigger>
                              <TooltipContent className="max-w-xs">
                                <p>
                                  Composite index measuring exposure to climate risks including droughts, floods, and
                                  sea-level rise. Higher scores indicate greater vulnerability.
                                </p>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        </div>
                        <span className="font-bold text-[#f59e0b]">
                          {country.climate_vulnerability_score.toFixed(1)}/100
                        </span>
                      </div>
                      <Progress value={country.climate_vulnerability_score} className="h-2 [&>div]:bg-[#f59e0b]" />
                    </div>

                    <div className="pt-4 border-t border-border/50">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <p className="text-xs text-muted-foreground">Sources: World Bank, IMF, UN Climate Index</p>
                          <TooltipProvider>
                            <Tooltip>
                              <TooltipTrigger>
                                <Info className="h-3 w-3 text-muted-foreground/60" />
                              </TooltipTrigger>
                              <TooltipContent className="max-w-xs">
                                <p className="font-semibold mb-1">Data Sources:</p>
                                <ul className="text-xs space-y-1">
                                  <li>• GDP: World Bank World Development Indicators</li>
                                  <li>• Population: UN Population Division</li>
                                  <li>• Climate: ND-GAIN Country Index</li>
                                  <li>• Debt: IMF World Economic Outlook</li>
                                </ul>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        </div>
                        {!usingFallbackData && (
                          <Badge variant="outline" className="text-xs border-green-500/30 text-green-700">
                            <div className="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5" />
                            Live
                          </Badge>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </>
        )}
      </main>

      <Footer />
    </div>
  )
}
