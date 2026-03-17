import Link from "next/link"
import { Globe, Github, FileText, Scale } from "lucide-react"

export function Footer() {
  return (
    <footer className="border-t border-border/40 bg-slate-50 mt-16">
      <div className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Branding */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <Globe className="h-5 w-5 text-[#1e3a5f]" />
              <h3 className="font-bold text-lg text-[#1e3a5f]">The Borrower's Forum Platform</h3>
            </div>
            <p className="text-sm text-muted-foreground">
              Data-driven debt intelligence for developing nations making strategic fiscal decisions.
            </p>
          </div>

          {/* Data Sources */}
          <div className="space-y-3">
            <h4 className="font-semibold text-sm text-slate-900">Data Sources</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li className="flex items-center gap-2">
                <div className="w-1 h-1 rounded-full bg-[#f59e0b]" />
                World Bank Open Data
              </li>
              <li className="flex items-center gap-2">
                <div className="w-1 h-1 rounded-full bg-[#f59e0b]" />
                International Monetary Fund (IMF)
              </li>
              <li className="flex items-center gap-2">
                <div className="w-1 h-1 rounded-full bg-[#f59e0b]" />
                Paris Club Secretariat
              </li>
              <li className="flex items-center gap-2">
                <div className="w-1 h-1 rounded-full bg-[#f59e0b]" />
                UN Climate Vulnerability Index
              </li>
            </ul>
          </div>

          {/* Links */}
          <div className="space-y-3">
            <h4 className="font-semibold text-sm text-slate-900">Resources</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link
                  href="/api-docs"
                  className="text-muted-foreground hover:text-[#1e3a5f] transition-colors flex items-center gap-2"
                >
                  <FileText className="h-3.5 w-3.5" />
                  API Documentation
                </Link>
              </li>
              <li>
                <Link
                  href="https://github.com/AnneNgarachu/Borrowers-Forum"
                  className="text-muted-foreground hover:text-[#1e3a5f] transition-colors flex items-center gap-2"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Github className="h-3.5 w-3.5" />
                  GitHub Repository
                </Link>
              </li>
              <li>
                <Link
                  href="/legal"
                  className="text-muted-foreground hover:text-[#1e3a5f] transition-colors flex items-center gap-2"
                >
                  <Scale className="h-3.5 w-3.5" />
                  Legal & Disclaimer
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Data Disclaimer */}
        <div className="border-t border-border/40 mt-8 pt-6">
          <div className="mb-4 text-xs text-slate-500 leading-relaxed">
            <strong className="text-slate-600">Data Disclaimer:</strong> All restructuring data is compiled from
            official sources including Paris Club press releases, IMF staff reports, and World Bank publications.
            Figures represent publicly reported values and may not reflect confidential terms.
          </div>
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-muted-foreground">
            <div className="flex flex-col sm:flex-row items-center gap-2">
              <p>© {new Date().getFullYear()} The Borrower's Forum Platform</p>
              <span className="hidden sm:inline text-slate-400">•</span>
              <p className="text-slate-500">Open Source Project</p>
              <span className="hidden sm:inline text-slate-400">•</span>
              <p className="text-slate-500">Database last updated: December 2024</p>
            </div>
            <p className="text-slate-600">
              Prototype developed by{" "}
              <a
                href="https://annengarachu.com"
                target="_blank"
                rel="noopener noreferrer"
                className="font-semibold text-[#1e3a5f] hover:text-blue-700 transition-colors underline decoration-dotted"
              >
                Anne Ngarachu
              </a>
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}
