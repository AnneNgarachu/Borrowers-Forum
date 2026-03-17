"use client"

import { Globe } from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"

export function Header() {
  const pathname = usePathname()

  const navItems = [
    { href: "/calculator", label: "Calculator" },
    { href: "/precedents", label: "Precedents" },
    { href: "/countries", label: "Countries" },
    { href: "/resources", label: "Resources" },
  ]

  return (
    <header className="border-b border-border/40 bg-gradient-to-r from-blue-50 via-blue-100 to-slate-100 sticky top-0 z-50 backdrop-blur-sm shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo - serves as home button */}
          <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity group">
            <div className="bg-blue-500/10 p-2 rounded-lg backdrop-blur-sm border border-blue-200 group-hover:bg-blue-500/20 transition-colors">
              <Globe className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-slate-800">The Borrower's Forum</h1>
              <p className="text-xs text-slate-600">Debt Intelligence Platform</p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "px-4 py-2 rounded-md text-sm font-medium transition-colors",
                  pathname === item.href
                    ? "bg-blue-500/10 text-blue-700 border border-blue-200"
                    : "text-slate-600 hover:text-blue-700 hover:bg-blue-500/5",
                )}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </header>
  )
}
