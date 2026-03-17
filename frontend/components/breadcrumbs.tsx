"use client"

import Link from "next/link"
import { ChevronRight, Home } from "lucide-react"
import { usePathname } from "next/navigation"

export function Breadcrumbs() {
  const pathname = usePathname()

  const pathSegments = pathname.split("/").filter(Boolean)

  // If on homepage, don't show breadcrumbs
  if (pathSegments.length === 0) {
    return null
  }

  const breadcrumbItems = [
    { label: "Home", href: "/" },
    ...pathSegments.map((segment, index) => {
      const href = `/${pathSegments.slice(0, index + 1).join("/")}`
      const label = segment
        .split("-")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ")

      return { label, href }
    }),
  ]

  return (
    <nav className="flex items-center gap-2 text-sm text-slate-600 mb-6">
      {breadcrumbItems.map((item, index) => (
        <div key={item.href} className="flex items-center gap-2">
          {index === 0 ? (
            <Link href={item.href} className="flex items-center gap-1 hover:text-blue-600 transition-colors">
              <Home className="h-4 w-4" />
              <span>{item.label}</span>
            </Link>
          ) : (
            <>
              <ChevronRight className="h-4 w-4 text-slate-400" />
              {index === breadcrumbItems.length - 1 ? (
                <span className="font-medium text-slate-900">{item.label}</span>
              ) : (
                <Link href={item.href} className="hover:text-blue-600 transition-colors">
                  {item.label}
                </Link>
              )}
            </>
          )}
        </div>
      ))}
    </nav>
  )
}
