"use server"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://borrowers-forum.onrender.com"
const API_KEY = process.env.API_KEY

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  if (!API_KEY) {
    return {
      error: true,
      status: 500,
      message: "API_KEY environment variable is not configured",
    }
  }

  try {
    const response = await fetch(url, {
      ...options,
      cache: "no-store", // Added cache: 'no-store' to prevent Next.js from caching and logging failed requests
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
        ...options.headers,
      },
    })

    if (!response.ok) {
      const errorText = await response.text()

      if (response.status === 404) {
        console.log("[v0] Resource not found (404), will use fallback data")
      } else {
        console.log("[v0] API Error:", response.status, errorText)
      }

      return {
        error: true,
        status: response.status,
        message: errorText,
      }
    }

    return response.json()
  } catch (error) {
    console.log("[v0] Network error, will use fallback data:", error instanceof Error ? error.message : String(error))
    return {
      error: true,
      status: 0,
      message: "Network request failed",
    }
  }
}

export interface Country {
  code: string
  name: string
  region: string
  income_level: string
  population: number
  gdp_usd_billions: number
  climate_vulnerability_score: number
}

export interface DebtCalculationRequest {
  country_code: string
  year: number
  debt_amount_usd: number
}

export interface DebtCalculationResponse {
  country_info: {
    code: string
    name: string
    region: string
    income_level: string
  }
  calculation: {
    debt_amount_usd: number
    year: number
  }
  equivalents: {
    doctors: {
      annual_employment: number
      five_year_employment: number
      annual_salary_usd: number
      description: string
    }
    schools: {
      number_of_schools: number
      cost_per_school_usd: number
      description: string
    }
    climate_adaptation: {
      percentage_of_annual_budget: number
      annual_climate_budget_usd: number
      description: string
    }
  }
  data_source: string
  data_year: number
}

export interface PrecedentSearchParams {
  country_code?: string
  year_start?: number
  year_end?: number
  creditor_type?: string
  treatment_type?: string
  includes_climate?: boolean
}

export interface Precedent {
  id: string
  country: {
    code: string
    name: string
    region: string
    income_level: string
  }
  year: number
  debt_amount_millions: number
  creditor_type: string
  treatment_type: string
  npv_reduction_percent: number
  grace_period_months: number
  includes_climate_clause: string
  terms_summary: string
}

export interface SimilarPrecedentsParams {
  country_code: string
  debt_amount_millions: number
}

export interface SimilarPrecedent {
  similarity_score: number
  score_breakdown: {
    regional_match: boolean
    income_level_match: boolean
    climate_vulnerability_similarity: number
    debt_amount_ratio: number
    years_ago: number
  }
  country: {
    code: string
    name: string
  }
  year: number
  debt_amount_millions: number
  creditor_type: string
  treatment_type: string
  npv_reduction_percent: number
  includes_climate_clause: string
}

export interface SimilarPrecedentsResponse {
  reference_country: {
    code: string
    name: string
  }
  reference_debt_amount_millions: number
  similar_precedents: SimilarPrecedent[]
  total_found: number
}

export interface PrecedentStats {
  total_precedents: number
  by_creditor_type: Record<string, number>
  by_treatment_type: Record<string, number>
  by_climate_clause: Record<string, number>
  year_range: {
    min: number
    max: number
  }
}

function calculateFallbackDebtEquivalents(countryCode: string, debtAmountUsd: number): DebtCalculationResponse {
  // Fallback salary and cost estimates based on income level
  const fallbackData: Record<string, { doctorSalary: number; schoolCost: number; climateBudget: number }> = {
    // Upper-Middle Income countries
    ARG: { doctorSalary: 45000, schoolCost: 800000, climateBudget: 2000000000 },
    BLZ: { doctorSalary: 35000, schoolCost: 500000, climateBudget: 50000000 },
    ECU: { doctorSalary: 40000, schoolCost: 600000, climateBudget: 500000000 },
    LBN: { doctorSalary: 38000, schoolCost: 550000, climateBudget: 300000000 },
    SUR: { doctorSalary: 42000, schoolCost: 650000, climateBudget: 80000000 },
    // Lower-Middle Income countries
    BGD: { doctorSalary: 18000, schoolCost: 200000, climateBudget: 1500000000 },
    EGY: { doctorSalary: 20000, schoolCost: 250000, climateBudget: 2500000000 },
    GHA: { doctorSalary: 22000, schoolCost: 300000, climateBudget: 400000000 },
    KEN: { doctorSalary: 24000, schoolCost: 350000, climateBudget: 800000000 },
    PAK: { doctorSalary: 16000, schoolCost: 180000, climateBudget: 3000000000 },
    SEN: { doctorSalary: 19000, schoolCost: 220000, climateBudget: 250000000 },
    ZMB: { doctorSalary: 21000, schoolCost: 280000, climateBudget: 300000000 },
    LKA: { doctorSalary: 17000, schoolCost: 190000, climateBudget: 600000000 },
    UKR: { doctorSalary: 25000, schoolCost: 400000, climateBudget: 1200000000 },
    // Low Income countries
    ETH: { doctorSalary: 12000, schoolCost: 150000, climateBudget: 500000000 },
    TCD: { doctorSalary: 10000, schoolCost: 120000, climateBudget: 150000000 },
    MOZ: { doctorSalary: 11000, schoolCost: 140000, climateBudget: 200000000 },
  }

  const countryDefaults = fallbackData[countryCode] || {
    doctorSalary: 20000,
    schoolCost: 300000,
    climateBudget: 500000000,
  }

  return {
    country_info: {
      code: countryCode,
      name: "Unknown",
      region: "Unknown",
      income_level: "Unknown",
    },
    calculation: {
      debt_amount_usd: debtAmountUsd,
      year: 2023,
    },
    equivalents: {
      doctors: {
        annual_employment: Math.round(debtAmountUsd / countryDefaults.doctorSalary),
        five_year_employment: Math.round((debtAmountUsd / countryDefaults.doctorSalary) * 5),
        annual_salary_usd: countryDefaults.doctorSalary,
        description: `Based on estimated healthcare worker costs for ${countryCode}`,
      },
      schools: {
        number_of_schools: Math.round(debtAmountUsd / countryDefaults.schoolCost),
        cost_per_school_usd: countryDefaults.schoolCost,
        description: `Based on estimated school construction costs for ${countryCode}`,
      },
      climate_adaptation: {
        percentage_of_annual_budget: (debtAmountUsd / countryDefaults.climateBudget) * 100,
        annual_climate_budget_usd: countryDefaults.climateBudget,
        description: `Based on estimated climate adaptation budget for ${countryCode}`,
      },
    },
    data_source: "Fallback Estimates (API Unavailable)",
    data_year: 2023,
  }
}

export async function getAllCountriesAction(): Promise<Country[]> {
  try {
    const data = await fetchWithAuth(`${API_BASE_URL}/api/v1/countries`)
    return data
  } catch (error) {
    console.error("[v0] Error fetching countries:", error)
    throw error
  }
}

export async function calculateDebtAction(request: DebtCalculationRequest): Promise<DebtCalculationResponse> {
  console.log("[v0] Calculate Debt Request:", request)

  const queryParams = new URLSearchParams({
    country_code: request.country_code,
    year: request.year.toString(),
    debt_amount_usd: request.debt_amount_usd.toString(),
  })

  const url = `${API_BASE_URL}/api/v1/debt/calculate-live?${queryParams.toString()}`
  console.log("[v0] Request URL:", url)

  try {
    const data = await fetchWithAuth(url, {
      method: "POST",
    })

    // Check if response contains an error
    if (data && typeof data === "object" && "error" in data) {
      console.log("[v0] API returned error, using fallback calculation for country:", request.country_code)
      return calculateFallbackDebtEquivalents(request.country_code, request.debt_amount_usd)
    }

    console.log("[v0] API Response:", data)
    return data
  } catch (error) {
    // Only log the error, don't throw - use fallback instead
    console.log("[v0] Using fallback calculation due to API error:", error)
    return calculateFallbackDebtEquivalents(request.country_code, request.debt_amount_usd)
  }
}

export async function searchPrecedentsAction(params: PrecedentSearchParams = {}): Promise<Precedent[]> {
  try {
    const queryParams = new URLSearchParams()

    if (params.country_code) queryParams.append("country_code", params.country_code)
    if (params.year_start) queryParams.append("year_start", params.year_start.toString())
    if (params.year_end) queryParams.append("year_end", params.year_end.toString())
    if (params.creditor_type) queryParams.append("creditor_type", params.creditor_type)
    if (params.treatment_type) queryParams.append("treatment_type", params.treatment_type)
    if (params.includes_climate !== undefined) {
      queryParams.append("includes_climate", params.includes_climate.toString())
    }

    const url = `${API_BASE_URL}/api/v1/precedents?${queryParams.toString()}`
    const data = await fetchWithAuth(url)
    return data
  } catch (error) {
    console.error("[v0] Error searching precedents:", error)
    throw error
  }
}

export async function findSimilarPrecedentsAction(params: SimilarPrecedentsParams): Promise<SimilarPrecedentsResponse> {
  try {
    const queryParams = new URLSearchParams({
      country_code: params.country_code,
      debt_amount_millions: params.debt_amount_millions.toString(),
    })

    const url = `${API_BASE_URL}/api/v1/precedents/similar?${queryParams.toString()}`
    const data = await fetchWithAuth(url)
    return data
  } catch (error) {
    console.error("[v0] Error finding similar precedents:", error)
    throw error
  }
}

export interface StrategyBriefRequest {
  country_code: string
  debt_amount_usd: number
  relief_percent: number
}

export interface StrategyBriefResponse {
  country: {
    code: string
    name: string
    region: string
    income_level: string
    climate_vulnerability_score: number
  }
  parameters: {
    debt_amount_usd: number
    relief_percent: number
    potential_savings_usd: number
  }
  brief: string
  precedents_used: number
  climate_precedents_used: number
}

export async function generateStrategyBriefAction(
  request: StrategyBriefRequest
): Promise<StrategyBriefResponse> {
  const url = `${API_BASE_URL}/api/v1/ai/strategy-brief`

  const data = await fetchWithAuth(url, {
    method: "POST",
    body: JSON.stringify(request),
  })

  if (data && typeof data === "object" && "error" in data) {
    throw new Error(data.message || "Failed to generate strategy brief")
  }

  return data
}

export async function getPrecedentStatsAction(): Promise<PrecedentStats> {
  try {
    const data = await fetchWithAuth(`${API_BASE_URL}/api/v1/precedents/stats`)
    return data
  } catch (error) {
    console.error("[v0] Error fetching precedent stats:", error)
    throw error
  }
}
