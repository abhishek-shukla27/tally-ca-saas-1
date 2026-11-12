"use client";

import React, { useState } from "react";
import {
  LayoutDashboard,
  Users,
  ShieldAlert,
  Search,
  Bell,
  CheckCircle2,
  AlertTriangle,
  FileSpreadsheet,
  ArrowUpRight,
  TrendingUp,
  Filter,
  Download,
  Building2,
  Calendar,
  Layers,
  ChevronRight,
  Menu,
  X,
  ExternalLink
} from "lucide-react";
import { MOCK_CLIENTS, MOCK_AUDIT_FLAGS, AuditFlagItem, ClientItem } from "@/data/mockData";

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<"overview" | "clients" | "compliance">("overview");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [severityFilter, setSeverityFilter] = useState<"ALL" | "CRITICAL" | "WARNING">("ALL");
  const [searchQuery, setSearchQuery] = useState("");

  const filteredFlags = MOCK_AUDIT_FLAGS.filter((flag) => {
    const matchesSeverity = severityFilter === "ALL" || flag.severity === severityFilter;
    const matchesSearch =
      flag.clientName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      flag.voucherRef.toLowerCase().includes(searchQuery.toLowerCase()) ||
      flag.ruleViolated.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesSeverity && matchesSearch;
  });

  const totalClientsCount = 12; // As requested in requirements
  const activeCriticalFlagsCount = 8; // As requested in requirements
  const totalVouchersMonitored = "1,420"; // As requested in requirements

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      {/* Mobile Sidebar Backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/50 backdrop-blur-sm lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar Navigation */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 flex w-72 flex-col border-r border-slate-200 bg-white transition-transform duration-200 lg:static lg:translate-x-0 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-0 max-lg:-translate-x-full"
        }`}
      >
        {/* Brand / Logo */}
        <div className="flex h-16 items-center justify-between border-b border-slate-200 px-6">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-600 text-white shadow-md shadow-indigo-600/20">
              <ShieldAlert className="h-5 w-5" />
            </div>
            <div>
              <span className="font-bold tracking-tight text-slate-900">TallyAudit</span>
              <span className="ml-1.5 rounded-full bg-indigo-50 px-2 py-0.5 text-xs font-semibold text-indigo-700 border border-indigo-100">
                CA Portal
              </span>
            </div>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 lg:hidden"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Firm / Workspace Context */}
        <div className="p-4">
          <div className="flex items-center gap-3 rounded-xl border border-slate-100 bg-slate-50/80 p-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-white border border-slate-200 text-slate-700 font-bold shadow-xs">
              SA
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-semibold text-slate-900">Sharma & Associates</p>
              <p className="truncate text-xs text-slate-500">Chartered Accountants</p>
            </div>
          </div>
        </div>

        {/* Navigation Routes */}
        <div className="flex-1 px-4 py-2 space-y-1">
          <button
            onClick={() => {
              setActiveTab("overview");
              setSidebarOpen(false);
            }}
            className={`flex w-full items-center gap-3 rounded-lg px-3.5 py-2.5 text-sm font-medium transition-all ${
              activeTab === "overview"
                ? "bg-indigo-50 text-indigo-700 shadow-xs border border-indigo-100/60"
                : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
            }`}
          >
            <LayoutDashboard className={`h-4 w-4 ${activeTab === "overview" ? "text-indigo-600" : "text-slate-400"}`} />
            Overview
          </button>

          <button
            onClick={() => {
              setActiveTab("clients");
              setSidebarOpen(false);
            }}
            className={`flex w-full items-center justify-between rounded-lg px-3.5 py-2.5 text-sm font-medium transition-all ${
              activeTab === "clients"
                ? "bg-indigo-50 text-indigo-700 shadow-xs border border-indigo-100/60"
                : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
            }`}
          >
            <div className="flex items-center gap-3">
              <Users className={`h-4 w-4 ${activeTab === "clients" ? "text-indigo-600" : "text-slate-400"}`} />
              Clients
            </div>
            <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-semibold text-slate-600">
              {totalClientsCount}
            </span>
          </button>

          <button
            onClick={() => {
              setActiveTab("compliance");
              setSidebarOpen(false);
            }}
            className={`flex w-full items-center justify-between rounded-lg px-3.5 py-2.5 text-sm font-medium transition-all ${
              activeTab === "compliance"
                ? "bg-indigo-50 text-indigo-700 shadow-xs border border-indigo-100/60"
                : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
            }`}
          >
            <div className="flex items-center gap-3">
              <ShieldAlert className={`h-4 w-4 ${activeTab === "compliance" ? "text-indigo-600" : "text-slate-400"}`} />
              Compliance Audit Desk
            </div>
            <span className="rounded-full bg-red-100 px-2 py-0.5 text-xs font-bold text-red-700">
              {activeCriticalFlagsCount}
            </span>
          </button>
        </div>

        {/* Live Ingestion Indicator at footer */}
        <div className="p-4 border-t border-slate-200">
          <div className="rounded-xl border border-emerald-100 bg-emerald-50/60 p-3.5">
            <div className="flex items-center gap-2 text-xs font-semibold text-emerald-800">
              <span className="relative flex h-2 w-2">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500"></span>
              </span>
              Tally Sync Daemon Live
            </div>
            <p className="mt-1 text-xs text-emerald-700/80">Local agent syncing on port 9000</p>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Top Header */}
        <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(true)}
              className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 lg:hidden"
            >
              <Menu className="h-5 w-5" />
            </button>
            <h1 className="text-lg font-bold text-slate-900">
              {activeTab === "overview" && "Executive Audit Overview"}
              {activeTab === "clients" && "Connected Client Accounts"}
              {activeTab === "compliance" && "Compliance Audit Desk"}
            </h1>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-medium text-slate-600">
              <Calendar className="h-3.5 w-3.5 text-slate-400" />
              FY 2024-2025 (Active)
            </div>
            <button className="relative rounded-lg p-2 text-slate-500 hover:bg-slate-100">
              <Bell className="h-5 w-5" />
              <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-red-600 ring-2 ring-white"></span>
            </button>
          </div>
        </header>

        {/* Scrollable Content */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8">
          {/* TAB 1: OVERVIEW */}
          {activeTab === "overview" && (
            <div className="space-y-8 max-w-7xl mx-auto">
              {/* Welcome banner */}
              <div className="rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 p-6 md:p-8 text-white shadow-xl">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                  <div className="space-y-2">
                    <div className="inline-flex items-center gap-2 rounded-full bg-indigo-500/20 px-3 py-1 text-xs font-medium text-indigo-300 border border-indigo-400/30">
                      Automated Tax & GST Vigilance
                    </div>
                    <h2 className="text-2xl font-bold tracking-tight text-white md:text-3xl">
                      Client Compliance Desk
                    </h2>
                    <p className="text-slate-300 text-sm max-w-2xl leading-relaxed">
                      Continuous real-time ingestion from client TallyPrime nodes. Flags Section 40A(3) cash expense breaches, invalid GSTIN syntax, and negative cash balances automatically.
                    </p>
                  </div>
                  <button
                    onClick={() => setActiveTab("compliance")}
                    className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-900 shadow-sm hover:bg-slate-100 transition"
                  >
                    Review Critical Flags
                    <ArrowUpRight className="h-4 w-4" />
                  </button>
                </div>
              </div>

              {/* 3 Required KPI Metric Cards */}
              <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
                {/* Metric 1 */}
                <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-xs hover:border-slate-300 transition">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-500">Total Clients Connected</span>
                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-50 text-blue-600 border border-blue-100">
                      <Users className="h-5 w-5" />
                    </div>
                  </div>
                  <div className="mt-4 flex items-baseline gap-2">
                    <span className="text-3xl font-extrabold tracking-tight text-slate-900">{totalClientsCount}</span>
                    <span className="inline-flex items-center text-xs font-semibold text-emerald-600">
                      <TrendingUp className="mr-0.5 h-3 w-3" /> +2 this month
                    </span>
                  </div>
                  <p className="mt-2 text-xs text-slate-500">Live sync agents configured across Windows PCs</p>
                </div>

                {/* Metric 2 */}
                <div className="rounded-xl border border-red-200/80 bg-red-50/20 p-6 shadow-xs hover:border-red-300 transition">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-600">Active Critical Audit Flags</span>
                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-red-100 text-red-600 border border-red-200">
                      <ShieldAlert className="h-5 w-5" />
                    </div>
                  </div>
                  <div className="mt-4 flex items-baseline gap-2">
                    <span className="text-3xl font-extrabold tracking-tight text-red-700">{activeCriticalFlagsCount}</span>
                    <span className="rounded-full bg-red-100 px-2 py-0.5 text-xs font-bold text-red-800">
                      Requires Action
                    </span>
                  </div>
                  <p className="mt-2 text-xs text-red-600/80">Sec 40A(3) breaches &amp; negative balances</p>
                </div>

                {/* Metric 3 */}
                <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-xs hover:border-slate-300 transition">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-500">Total Vouchers Monitored</span>
                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 border border-emerald-100">
                      <FileSpreadsheet className="h-5 w-5" />
                    </div>
                  </div>
                  <div className="mt-4 flex items-baseline gap-2">
                    <span className="text-3xl font-extrabold tracking-tight text-slate-900">{totalVouchersMonitored}</span>
                    <span className="inline-flex items-center text-xs font-semibold text-emerald-600">
                      100% Parsed
                    </span>
                  </div>
                  <p className="mt-2 text-xs text-slate-500">Ingested via XML stream from Tally instances</p>
                </div>
              </div>

              {/* Recent Audit Anomalies Preview */}
              <div className="rounded-xl border border-slate-200 bg-white shadow-xs">
                <div className="flex items-center justify-between border-b border-slate-200 px-6 py-4">
                  <div>
                    <h3 className="font-semibold text-slate-900">Recent High-Priority Flags</h3>
                    <p className="text-xs text-slate-500">Latest exceptions requiring CA intervention</p>
                  </div>
                  <button
                    onClick={() => setActiveTab("compliance")}
                    className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 flex items-center gap-1"
                  >
                    View All in Desk <ChevronRight className="h-3.5 w-3.5" />
                  </button>
                </div>

                <div className="divide-y divide-slate-100">
                  {MOCK_AUDIT_FLAGS.slice(0, 4).map((flag) => (
                    <div key={flag.id} className="flex flex-col sm:flex-row sm:items-center justify-between p-4 px-6 hover:bg-slate-50/80 transition gap-3">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-sm text-slate-900">{flag.clientName}</span>
                          <span className="text-xs text-slate-400">•</span>
                          <span className="text-xs font-mono text-slate-600 font-medium">{flag.voucherRef}</span>
                          <span
                            className={`rounded-full px-2 py-0.5 text-[10px] font-bold tracking-wide uppercase ${
                              flag.severity === "CRITICAL"
                                ? "bg-red-100 text-red-700 border border-red-200"
                                : "bg-amber-100 text-amber-800 border border-amber-200"
                            }`}
                          >
                            {flag.severity}
                          </span>
                        </div>
                        <p className="text-xs text-slate-600">{flag.ruleViolated}</p>
                      </div>

                      <div className="text-right sm:self-center">
                        {flag.disallowedAmount > 0 ? (
                          <div className="text-sm font-bold text-red-600">
                            ₹{flag.disallowedAmount.toLocaleString("en-IN")}
                          </div>
                        ) : (
                          <div className="text-xs font-medium text-slate-500">Syntax Check</div>
                        )}
                        <span className="text-[11px] text-slate-400">{flag.date}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: CLIENTS */}
          {activeTab === "clients" && (
            <div className="space-y-6 max-w-7xl mx-auto">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h2 className="text-xl font-bold text-slate-900">Connected Tally Instances</h2>
                  <p className="text-xs text-slate-500">Client companies streaming data to this CA workspace</p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-medium text-slate-500">Auto-refresh every 60m</span>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                {MOCK_CLIENTS.map((client) => (
                  <div key={client.id} className="rounded-xl border border-slate-200 bg-white p-5 shadow-xs hover:border-slate-300 transition">
                    <div className="flex items-start justify-between">
                      <div className="space-y-1">
                        <h3 className="font-semibold text-slate-900 text-sm">{client.companyName}</h3>
                        <p className="text-xs font-mono text-slate-500">{client.panOrGstin}</p>
                      </div>
                      <span
                        className={`rounded-full px-2 py-0.5 text-xs font-semibold ${
                          client.status === "Active"
                            ? "bg-emerald-100 text-emerald-700"
                            : "bg-amber-100 text-amber-800"
                        }`}
                      >
                        {client.status}
                      </span>
                    </div>

                    <div className="mt-4 grid grid-cols-2 gap-2 border-t border-slate-100 pt-3 text-xs">
                      <div>
                        <span className="text-slate-400">Vouchers</span>
                        <p className="font-semibold text-slate-700">{client.totalVouchers}</p>
                      </div>
                      <div>
                        <span className="text-slate-400">Critical Flags</span>
                        <p className={`font-semibold ${client.criticalFlags > 0 ? "text-red-600" : "text-emerald-600"}`}>
                          {client.criticalFlags}
                        </p>
                      </div>
                    </div>

                    <div className="mt-3 flex items-center justify-between border-t border-slate-100 pt-3 text-[11px] text-slate-400">
                      <span>Last sync: {client.lastSync}</span>
                      <button
                        onClick={() => setActiveTab("compliance")}
                        className="font-medium text-indigo-600 hover:text-indigo-800 flex items-center gap-1"
                      >
                        Audit items <ChevronRight className="h-3 w-3" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 3: COMPLIANCE AUDIT DESK */}
          {activeTab === "compliance" && (
            <div className="space-y-6 max-w-7xl mx-auto">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <h2 className="text-xl font-bold text-slate-900">Compliance Audit Desk</h2>
                  <p className="text-xs text-slate-500">
                    Rule-based anomaly detection scanner running across all ingested vouchers
                  </p>
                </div>

                <div className="flex flex-wrap items-center gap-2">
                  {/* Severity Filter Buttons */}
                  <div className="flex rounded-lg border border-slate-200 bg-white p-1 shadow-2xs">
                    <button
                      onClick={() => setSeverityFilter("ALL")}
                      className={`rounded-md px-3 py-1 text-xs font-medium transition ${
                        severityFilter === "ALL" ? "bg-slate-900 text-white" : "text-slate-600 hover:text-slate-900"
                      }`}
                    >
                      All ({MOCK_AUDIT_FLAGS.length})
                    </button>
                    <button
                      onClick={() => setSeverityFilter("CRITICAL")}
                      className={`rounded-md px-3 py-1 text-xs font-medium transition ${
                        severityFilter === "CRITICAL" ? "bg-red-600 text-white" : "text-slate-600 hover:text-slate-900"
                      }`}
                    >
                      Critical (6)
                    </button>
                    <button
                      onClick={() => setSeverityFilter("WARNING")}
                      className={`rounded-md px-3 py-1 text-xs font-medium transition ${
                        severityFilter === "WARNING" ? "bg-amber-600 text-white" : "text-slate-600 hover:text-slate-900"
                      }`}
                    >
                      Warnings (2)
                    </button>
                  </div>

                  <button className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50">
                    <Download className="h-3.5 w-3.5" />
                    Export CSV
                  </button>
                </div>
              </div>

              {/* Search & Filter Bar */}
              <div className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-2.5 shadow-xs">
                <Search className="h-4 w-4 text-slate-400 ml-2" />
                <input
                  type="text"
                  placeholder="Filter by company, voucher reference, or rule (e.g. 40A(3), GSTIN)..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-transparent text-xs text-slate-900 outline-none placeholder:text-slate-400"
                />
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery("")}
                    className="text-xs text-slate-400 hover:text-slate-600 mr-2"
                  >
                    Clear
                  </button>
                )}
              </div>

              {/* Required Responsive Compliance Table */}
              <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-xs">
                <div className="overflow-x-auto">
                  <table className="w-full text-left border-collapse">
                    <thead>
                      <tr className="border-b border-slate-200 bg-slate-50/75 text-xs font-semibold text-slate-600">
                        <th className="py-3.5 pl-6 pr-3">Client Name</th>
                        <th className="py-3.5 px-3">Date</th>
                        <th className="py-3.5 px-3">Voucher Ref #</th>
                        <th className="py-3.5 px-3">Rule Violated</th>
                        <th className="py-3.5 px-3">Severity</th>
                        <th className="py-3.5 px-3 text-right">Disallowed / Value</th>
                        <th className="py-3.5 pl-3 pr-6">Detail / Ledger</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 text-xs">
                      {filteredFlags.length > 0 ? (
                        filteredFlags.map((item) => (
                          <tr key={item.id} className="hover:bg-slate-50/75 transition">
                            {/* Client Name */}
                            <td className="py-3.5 pl-6 pr-3 font-semibold text-slate-900 whitespace-nowrap">
                              {item.clientName}
                            </td>

                            {/* Date */}
                            <td className="py-3.5 px-3 text-slate-600 whitespace-nowrap font-medium">
                              {item.date}
                            </td>

                            {/* Voucher Ref */}
                            <td className="py-3.5 px-3 font-mono font-semibold text-indigo-700 whitespace-nowrap">
                              {item.voucherRef}
                            </td>

                            {/* Rule Violated */}
                            <td className="py-3.5 px-3 font-medium text-slate-800 whitespace-nowrap">
                              {item.ruleViolated}
                            </td>

                            {/* Severity Badge */}
                            <td className="py-3.5 px-3 whitespace-nowrap">
                              {item.severity === "CRITICAL" ? (
                                <span className="inline-flex items-center rounded-full bg-red-100 px-2.5 py-0.5 text-[11px] font-bold text-red-700 border border-red-200">
                                  Critical Violation
                                </span>
                              ) : (
                                <span className="inline-flex items-center rounded-full bg-amber-100 px-2.5 py-0.5 text-[11px] font-bold text-amber-800 border border-amber-200">
                                  Warning
                                </span>
                              )}
                            </td>

                            {/* Disallowed Amount */}
                            <td className="py-3.5 px-3 text-right whitespace-nowrap font-bold text-slate-900">
                              {item.disallowedAmount > 0 ? (
                                <span className="text-red-600">
                                  ₹{item.disallowedAmount.toLocaleString("en-IN")}
                                </span>
                              ) : (
                                <span className="text-slate-400 font-normal">N/A</span>
                              )}
                            </td>

                            {/* Detail & Ledger */}
                            <td className="py-3.5 pl-3 pr-6 text-slate-600 max-w-xs truncate">
                              <span className="font-semibold text-slate-800 mr-1.5">{item.partyLedger}:</span>
                              {item.detail}
                            </td>
                          </tr>
                        ))
                      ) : (
                        <tr>
                          <td colSpan={7} className="py-12 text-center text-slate-400">
                            No flagged compliance violations match your filter criteria.
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>

                {/* Table Footer info */}
                <div className="flex items-center justify-between border-t border-slate-200 bg-slate-50/50 px-6 py-3 text-xs text-slate-500">
                  <span>
                    Showing {filteredFlags.length} of {MOCK_AUDIT_FLAGS.length} flagged vouchers
                  </span>
                  <span>Rule Engine v1.0.4 Active</span>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

