"""
Borrower's Forum Platform - External Data Service
==================================================

Fetches real economic data from public APIs:
- World Bank API: GDP, Population, Economic indicators
- IMF API: Debt statistics

All APIs are free and don't require authentication.
"""

import requests
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ExternalDataError(Exception):
    """Exception for external data fetching errors."""
    pass


class WorldBankAPI:
    """
    World Bank Open Data API client.
    
    Documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
    
    Indicators used:
    - NY.GDP.MKTP.CD: GDP (current US$)
    - SP.POP.TOTL: Population, total
    - DT.DOD.DECT.CD: External debt stocks, total (DOD, current US$)
    - DT.TDS.DECT.CD: Total debt service (current US$)
    - GC.REV.XGRT.GD.ZS: Revenue (% of GDP)
    """
    
    BASE_URL = "https://api.worldbank.org/v2"
    
    # World Bank indicator codes
    INDICATORS = {
        "gdp": "NY.GDP.MKTP.CD",
        "population": "SP.POP.TOTL",
        "external_debt": "DT.DOD.DECT.CD",
        "debt_service": "DT.TDS.DECT.CD",
        "revenue_pct_gdp": "GC.REV.XGRT.GD.ZS",
    }
    
    # Cache to avoid repeated API calls (simple in-memory cache)
    _cache: Dict[str, Any] = {}
    _cache_ttl = timedelta(hours=1)
    _cache_timestamps: Dict[str, datetime] = {}
    
    @classmethod
    def _get_cached(cls, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        if key in cls._cache:
            timestamp = cls._cache_timestamps.get(key)
            if timestamp and datetime.now() - timestamp < cls._cache_ttl:
                return cls._cache[key]
        return None
    
    @classmethod
    def _set_cached(cls, key: str, value: Any):
        """Set cached value with timestamp."""
        cls._cache[key] = value
        cls._cache_timestamps[key] = datetime.now()
    
    @classmethod
    def get_indicator(
        cls,
        country_code: str,
        indicator: str,
        year: Optional[int] = None
    ) -> Optional[float]:
        """
        Fetch a single indicator value for a country.
        
        Args:
            country_code: ISO 3-letter country code (e.g., "GHA")
            indicator: Indicator key (e.g., "gdp", "population")
            year: Specific year (None = most recent)
        
        Returns:
            Indicator value or None if not found
        """
        indicator_code = cls.INDICATORS.get(indicator)
        if not indicator_code:
            raise ExternalDataError(f"Unknown indicator: {indicator}")
        
        # Check cache
        cache_key = f"{country_code}_{indicator}_{year}"
        cached = cls._get_cached(cache_key)
        if cached is not None:
            return cached
        
        try:
            # Build URL
            url = f"{cls.BASE_URL}/country/{country_code}/indicator/{indicator_code}"
            params = {
                "format": "json",
                "per_page": 10,
                "date": str(year) if year else None
            }
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # World Bank returns [metadata, data_array]
            if len(data) < 2 or not data[1]:
                logger.warning(f"No data found for {country_code}/{indicator}")
                return None
            
            # Get most recent non-null value
            for record in data[1]:
                if record.get("value") is not None:
                    value = float(record["value"])
                    cls._set_cached(cache_key, value)
                    return value
            
            return None
            
        except requests.RequestException as e:
            logger.error(f"World Bank API error: {e}")
            raise ExternalDataError(f"Failed to fetch {indicator} for {country_code}: {e}")
    
    @classmethod
    def get_country_data(cls, country_code: str, year: Optional[int] = None) -> Dict[str, Any]:
        """
        Fetch multiple indicators for a country.
        
        Args:
            country_code: ISO 3-letter country code
            year: Specific year (None = most recent)
        
        Returns:
            Dictionary with all available indicators
        """
        result = {
            "country_code": country_code,
            "year": year,
            "fetched_at": datetime.now().isoformat(),
            "source": "World Bank Open Data API"
        }
        
        for indicator_name in cls.INDICATORS.keys():
            try:
                value = cls.get_indicator(country_code, indicator_name, year)
                result[indicator_name] = value
            except ExternalDataError:
                result[indicator_name] = None
        
        return result
    
    @classmethod
    def get_country_info(cls, country_code: str) -> Optional[Dict[str, Any]]:
        """
        Fetch country metadata from World Bank.
        
        Args:
            country_code: ISO 3-letter country code
        
        Returns:
            Country info dict or None
        """
        cache_key = f"country_info_{country_code}"
        cached = cls._get_cached(cache_key)
        if cached:
            return cached
        
        try:
            url = f"{cls.BASE_URL}/country/{country_code}"
            params = {"format": "json"}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if len(data) < 2 or not data[1]:
                return None
            
            country = data[1][0]
            result = {
                "code": country.get("id"),
                "name": country.get("name"),
                "region": country.get("region", {}).get("value"),
                "income_level": country.get("incomeLevel", {}).get("id"),
                "capital": country.get("capitalCity"),
                "longitude": country.get("longitude"),
                "latitude": country.get("latitude"),
            }
            
            cls._set_cached(cache_key, result)
            return result
            
        except requests.RequestException as e:
            logger.error(f"World Bank country API error: {e}")
            return None


class IMFAPI:
    """
    IMF Data API client.
    
    Documentation: https://datahelp.imf.org/knowledgebase/articles/667681
    
    Datasets:
    - IFS: International Financial Statistics
    - DOT: Direction of Trade Statistics
    - GFS: Government Finance Statistics
    """
    
    BASE_URL = "http://dataservices.imf.org/REST/SDMX_JSON.svc"
    
    # Cache
    _cache: Dict[str, Any] = {}
    _cache_ttl = timedelta(hours=1)
    _cache_timestamps: Dict[str, datetime] = {}
    
    @classmethod
    def _get_cached(cls, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        if key in cls._cache:
            timestamp = cls._cache_timestamps.get(key)
            if timestamp and datetime.now() - timestamp < cls._cache_ttl:
                return cls._cache[key]
        return None
    
    @classmethod
    def _set_cached(cls, key: str, value: Any):
        """Set cached value with timestamp."""
        cls._cache[key] = value
        cls._cache_timestamps[key] = datetime.now()
    
    @classmethod
    def get_debt_service_data(
        cls,
        country_code: str,
        start_year: int = 2015,
        end_year: int = 2024
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch debt service data from IMF.
        
        Note: IMF uses 2-letter country codes for some endpoints.
        
        Args:
            country_code: ISO country code
            start_year: Start year
            end_year: End year
        
        Returns:
            Debt service data dict or None
        """
        cache_key = f"imf_debt_{country_code}_{start_year}_{end_year}"
        cached = cls._get_cached(cache_key)
        if cached:
            return cached
        
        try:
            # IMF IFS dataset for debt indicators
            # Using Government Finance Statistics (GFS)
            url = f"{cls.BASE_URL}/CompactData/GFS/A.{country_code}.W0_S1_G1120"
            
            response = requests.get(url, timeout=15)
            
            if response.status_code != 200:
                logger.warning(f"IMF API returned {response.status_code} for {country_code}")
                return None
            
            data = response.json()
            
            # Parse IMF SDMX-JSON response
            result = {
                "country_code": country_code,
                "source": "IMF Government Finance Statistics",
                "data": []
            }
            
            # Navigate complex IMF response structure
            try:
                series = data.get("CompactData", {}).get("DataSet", {}).get("Series", {})
                if series:
                    obs = series.get("Obs", [])
                    if isinstance(obs, dict):
                        obs = [obs]
                    
                    for ob in obs:
                        year = ob.get("@TIME_PERIOD")
                        value = ob.get("@OBS_VALUE")
                        if year and value:
                            result["data"].append({
                                "year": int(year),
                                "value": float(value)
                            })
            except (KeyError, TypeError) as e:
                logger.warning(f"Error parsing IMF data: {e}")
            
            cls._set_cached(cache_key, result)
            return result
            
        except requests.RequestException as e:
            logger.error(f"IMF API error: {e}")
            return None


class ExternalDataService:
    """
    Unified service for fetching external data.
    
    Combines data from multiple sources and provides
    a clean interface for the application.
    """
    
    def __init__(self):
        self.world_bank = WorldBankAPI
        self.imf = IMFAPI
    
    def get_country_economic_data(
        self,
        country_code: str,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive economic data for a country.
        
        Combines data from World Bank and IMF.
        
        Args:
            country_code: ISO 3-letter country code
            year: Specific year (None = most recent)
        
        Returns:
            Combined economic data
        """
        # Get World Bank data
        wb_data = self.world_bank.get_country_data(country_code, year)
        
        # Get country info
        country_info = self.world_bank.get_country_info(country_code)
        
        # Combine results
        result = {
            "country": country_info,
            "economic_indicators": {
                "gdp_usd": wb_data.get("gdp"),
                "population": wb_data.get("population"),
                "external_debt_usd": wb_data.get("external_debt"),
                "debt_service_usd": wb_data.get("debt_service"),
                "revenue_pct_gdp": wb_data.get("revenue_pct_gdp"),
            },
            "metadata": {
                "year": year,
                "fetched_at": datetime.now().isoformat(),
                "sources": ["World Bank Open Data API"]
            }
        }
        
        # Calculate derived metrics
        gdp = wb_data.get("gdp")
        revenue_pct = wb_data.get("revenue_pct_gdp")
        
        if gdp and revenue_pct:
            result["economic_indicators"]["government_revenue_usd"] = gdp * (revenue_pct / 100)
        
        return result
    
    def get_live_debt_data(
        self,
        country_code: str,
        year: int
    ) -> Dict[str, Any]:
        """
        Get live debt data for debt calculator.
        
        Returns data in format compatible with DebtData model.
        
        Args:
            country_code: ISO 3-letter country code
            year: Year for data
        
        Returns:
            Debt data dict compatible with calculator
        """
        wb_data = self.world_bank.get_country_data(country_code, year)
        
        # Convert to millions for consistency with our database
        gdp = wb_data.get("gdp")
        debt_service = wb_data.get("debt_service")
        revenue_pct = wb_data.get("revenue_pct_gdp")
        
        result = {
            "country_code": country_code,
            "year": year,
            "debt_service_usd_millions": debt_service / 1_000_000 if debt_service else None,
            "gdp_usd_millions": gdp / 1_000_000 if gdp else None,
            "government_revenue_usd_millions": (gdp * revenue_pct / 100) / 1_000_000 if gdp and revenue_pct else None,
            "source": "World Bank Open Data API (Live)",
            "fetched_at": datetime.now().isoformat()
        }
        
        return result


# ==========================================
# DEVELOPER NOTES
# ==========================================
"""
EXTERNAL DATA SERVICE USAGE:

from src.services.external_data import ExternalDataService

service = ExternalDataService()

# Get economic data for Ghana
data = service.get_country_economic_data("GHA", 2023)
print(f"Ghana GDP: ${data['economic_indicators']['gdp_usd']:,.0f}")

# Get debt data for Kenya
debt_data = service.get_live_debt_data("KEN", 2022)
print(f"Kenya Debt Service: ${debt_data['debt_service_usd_millions']:.1f}M")


CACHING:
- Data is cached in memory for 1 hour
- Reduces API calls and improves response time
- Cache resets when server restarts

ERROR HANDLING:
- Returns None for missing data (doesn't break calculations)
- Logs errors for debugging
- Gracefully degrades if APIs are unavailable

API RATE LIMITS:
- World Bank: No strict limit, but be respectful
- IMF: No strict limit, but responses can be slow
"""