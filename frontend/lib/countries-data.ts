export interface CountryProfile {
  code: string
  name: string
  region: string
  income_level: string
  gdp_usd_billions: number
  population: number
  climate_vulnerability_score: number
  debt_to_gdp_percent: number
  summary: string
  key_sectors: string[]
  gdp_growth_rate?: number
}

// Factual country data from World Bank, IMF, and UN sources (2023 estimates)
export const COUNTRY_PROFILES: CountryProfile[] = [
  {
    code: "BGD",
    name: "Bangladesh",
    region: "South Asia",
    income_level: "Lower-Middle Income",
    gdp_usd_billions: 460.2,
    population: 171190000,
    climate_vulnerability_score: 86.4,
    debt_to_gdp_percent: 39.6,
    summary:
      "Rapidly growing economy vulnerable to sea-level rise. Climate adaptation critical for 160M people in low-lying coastal areas.",
    key_sectors: ["Textiles", "Remittances", "Agriculture", "Pharmaceuticals"],
    gdp_growth_rate: 6.0,
  },
  {
    code: "EGY",
    name: "Egypt",
    region: "Middle East & North Africa",
    income_level: "Lower-Middle Income",
    gdp_usd_billions: 398.4,
    population: 110990000,
    climate_vulnerability_score: 64.2,
    debt_to_gdp_percent: 89.6,
    summary:
      "Most populous Arab nation with diversified economy. Faces foreign exchange pressures and climate risks to Nile Delta agriculture.",
    key_sectors: ["Tourism", "Natural Gas", "Manufacturing", "Suez Canal"],
    gdp_growth_rate: 3.8,
  },
  {
    code: "ETH",
    name: "Ethiopia",
    region: "Sub-Saharan Africa",
    income_level: "Low Income",
    gdp_usd_billions: 126.8,
    population: 123380000,
    climate_vulnerability_score: 77.9,
    debt_to_gdp_percent: 53.2,
    summary:
      "Second most populous African nation with fast-growing economy. Secured Common Framework treatment in 2021 amid conflict and drought.",
    key_sectors: ["Agriculture", "Coffee", "Manufacturing", "Hydropower"],
    gdp_growth_rate: 6.3,
  },
  {
    code: "GHA",
    name: "Ghana",
    region: "Sub-Saharan Africa",
    income_level: "Lower-Middle Income",
    gdp_usd_billions: 76.4,
    population: 33480000,
    climate_vulnerability_score: 68.5,
    debt_to_gdp_percent: 88.1,
    summary:
      "Major gold and cocoa exporter facing debt sustainability challenges. Secured $3B IMF program in 2023 for economic recovery and climate resilience.",
    key_sectors: ["Gold", "Cocoa", "Oil", "Services"],
    gdp_growth_rate: 2.9,
  },
  {
    code: "KEN",
    name: "Kenya",
    region: "Sub-Saharan Africa",
    income_level: "Lower-Middle Income",
    gdp_usd_billions: 115.4,
    population: 54030000,
    climate_vulnerability_score: 72.3,
    debt_to_gdp_percent: 67.3,
    summary:
      "East African economic hub with growing tech sector. Vulnerable to climate shocks affecting agriculture, which employs 75% of the workforce.",
    key_sectors: ["Agriculture", "Tourism", "Technology", "Finance"],
    gdp_growth_rate: 5.3,
  },
  {
    code: "PAK",
    name: "Pakistan",
    region: "South Asia",
    income_level: "Lower-Middle Income",
    gdp_usd_billions: 374.9,
    population: 235820000,
    climate_vulnerability_score: 81.7,
    debt_to_gdp_percent: 74.3,
    summary:
      "Fifth most populous country highly vulnerable to climate disasters. 2022 floods caused $30B in damages, affecting 33 million people.",
    key_sectors: ["Textiles", "Agriculture", "Remittances", "Services"],
    gdp_growth_rate: 2.1,
  },
  {
    code: "SEN",
    name: "Senegal",
    region: "Sub-Saharan Africa",
    income_level: "Lower-Middle Income",
    gdp_usd_billions: 27.6,
    population: 17320000,
    climate_vulnerability_score: 69.8,
    debt_to_gdp_percent: 73.6,
    summary:
      "West African democracy with emerging oil and gas sector. Coastal erosion threatens fishing communities and major economic centers.",
    key_sectors: ["Fishing", "Phosphates", "Tourism", "Oil & Gas"],
    gdp_growth_rate: 4.0,
  },
  {
    code: "ZMB",
    name: "Zambia",
    region: "Sub-Saharan Africa",
    income_level: "Lower-Middle Income",
    gdp_usd_billions: 29.8,
    population: 20020000,
    climate_vulnerability_score: 75.1,
    debt_to_gdp_percent: 123.4,
    summary:
      "Copper-dependent economy that became first African country to default during pandemic. Secured Common Framework debt treatment in 2023.",
    key_sectors: ["Copper", "Agriculture", "Mining", "Energy"],
    gdp_growth_rate: 4.7,
  },
  {
    code: "ARG",
    name: "Argentina",
    region: "Latin America & Caribbean",
    income_level: "Upper-Middle Income",
    gdp_usd_billions: 632.8,
    population: 45810000,
    climate_vulnerability_score: 52.3,
    debt_to_gdp_percent: 79.4,
    summary:
      "Major Latin American economy with recurring debt challenges. Secured 22nd IMF program in 2022 following sovereign default and currency crisis.",
    key_sectors: ["Agriculture", "Beef", "Lithium", "Services"],
    gdp_growth_rate: -1.6,
  },
  {
    code: "BLZ",
    name: "Belize",
    region: "Latin America & Caribbean",
    income_level: "Upper-Middle Income",
    gdp_usd_billions: 3.2,
    population: 405000,
    climate_vulnerability_score: 78.5,
    debt_to_gdp_percent: 66.2,
    summary:
      "Small Caribbean economy pioneering debt-for-nature swaps. Restructured $553M in bonds to fund marine conservation in 2021.",
    key_sectors: ["Tourism", "Agriculture", "Marine Resources", "Services"],
    gdp_growth_rate: 4.5,
  },
  {
    code: "TCD",
    name: "Chad",
    region: "Sub-Saharan Africa",
    income_level: "Low Income",
    gdp_usd_billions: 11.8,
    population: 17720000,
    climate_vulnerability_score: 82.7,
    debt_to_gdp_percent: 52.1,
    summary:
      "Oil-dependent Sahel nation facing severe climate stress. Lake Chad has shrunk 90% since 1960s, affecting 30 million people in region.",
    key_sectors: ["Oil", "Agriculture", "Livestock", "Cotton"],
    gdp_growth_rate: 3.1,
  },
  {
    code: "ECU",
    name: "Ecuador",
    region: "Latin America & Caribbean",
    income_level: "Upper-Middle Income",
    gdp_usd_billions: 115.0,
    population: 18000000,
    climate_vulnerability_score: 66.4,
    debt_to_gdp_percent: 58.9,
    summary:
      "Dollarized economy with oil dependence. Completed major debt-for-nature swap in 2023, freeing $1.1B for Galapagos conservation.",
    key_sectors: ["Oil", "Bananas", "Shrimp", "Tourism"],
    gdp_growth_rate: 2.4,
  },
  {
    code: "LBN",
    name: "Lebanon",
    region: "Middle East & North Africa",
    income_level: "Upper-Middle Income",
    gdp_usd_billions: 21.8,
    population: 5490000,
    climate_vulnerability_score: 61.9,
    debt_to_gdp_percent: 183.6,
    summary:
      "Facing severe economic crisis since 2019 with currency collapse and banking sector failure. Debt restructuring negotiations ongoing.",
    key_sectors: ["Banking", "Tourism", "Services", "Real Estate"],
    gdp_growth_rate: -0.6,
  },
  {
    code: "MOZ",
    name: "Mozambique",
    region: "Sub-Saharan Africa",
    income_level: "Low Income",
    gdp_usd_billions: 20.5,
    population: 32970000,
    climate_vulnerability_score: 84.2,
    debt_to_gdp_percent: 92.8,
    summary:
      "Gas-rich nation recovering from cyclone disasters and debt crisis. Extreme vulnerability to climate shocks with 60% coastal population.",
    key_sectors: ["Natural Gas", "Coal", "Agriculture", "Fishing"],
    gdp_growth_rate: 4.5,
  },
  {
    code: "LKA",
    name: "Sri Lanka",
    region: "South Asia",
    income_level: "Lower-Middle Income",
    gdp_usd_billions: 74.4,
    population: 22180000,
    climate_vulnerability_score: 73.6,
    debt_to_gdp_percent: 128.2,
    summary:
      "Island nation that defaulted in 2022 amid economic crisis. Negotiating debt restructuring under IMF program while facing climate risks.",
    key_sectors: ["Tea", "Textiles", "Tourism", "Remittances"],
    gdp_growth_rate: -7.8,
  },
  {
    code: "SUR",
    name: "Suriname",
    region: "Latin America & Caribbean",
    income_level: "Upper-Middle Income",
    gdp_usd_billions: 3.6,
    population: 618000,
    climate_vulnerability_score: 71.4,
    debt_to_gdp_percent: 124.3,
    summary:
      "Small Caribbean economy rich in resources. Restructured $675M in debt in 2023 with climate resilience provisions.",
    key_sectors: ["Oil", "Gold", "Bauxite", "Agriculture"],
    gdp_growth_rate: 1.9,
  },
  {
    code: "UKR",
    name: "Ukraine",
    region: "Europe & Central Asia",
    income_level: "Lower-Middle Income",
    gdp_usd_billions: 160.5,
    population: 43310000,
    climate_vulnerability_score: 48.2,
    debt_to_gdp_percent: 78.5,
    summary:
      "War-torn economy securing international support. Debt service suspended through 2024 with plans for comprehensive restructuring.",
    key_sectors: ["Agriculture", "Steel", "Technology", "Manufacturing"],
    gdp_growth_rate: -29.1,
  },
]
