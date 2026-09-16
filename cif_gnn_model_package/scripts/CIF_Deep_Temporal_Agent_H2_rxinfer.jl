#!/usr/bin/env julia
# RxInfer.jl ONLINE active-inference POMDP simulation — per-timestep infer()
# Generated from GNN Model: CIF_Deep_Temporal_Agent_H2
#
# Online mode (roadmap A1): at every timestep t, infer() runs on the
# observation prefix y[1:t]; the FILTERED posterior at t drives EFE action
# selection for the next step. Beliefs below are filtered (not smoothed).

using Pkg
using RxInfer
using Distributions
using LinearAlgebra
using Random
using SHA
using StatsBase
using JSON
using Base64
using Dates

const PLOTS_READY = try
@eval using Plots
true
catch e
println("⚠️ Plots unavailable; PNG plotting disabled: $e")
false
end

const SCHEMA_VERSION = "rxinfer_simulation_v1"
const MODEL_NAME = "CIF_Deep_Temporal_Agent_H2"
const NUM_STATES = 6
const NUM_OBSERVATIONS = 5
const NUM_ACTIONS = 4
const TIME_STEPS = 25
const RANDOM_SEED = 42
const ACTION_PRECISION = 2.5
const INFERENCE_ITERATIONS = 20
const B_TENSOR_ORDER = "next_state_previous_state_action"
const MODEL_KIND = "flat"
const INFERENCE_MODE = "online"
const GNN_SPEC_JSON_B64 = "eyJjYW5vbmljYWxfcG9tZHBfc2NoZW1hIjogImNhbm9uaWNhbF9wb21kcF92MSIsICJjb25uZWN0aW9ucyI6IFt7InJlbGF0aW9uIjogIi0iLCAic291cmNlIjogIkQiLCAidGFyZ2V0IjogInMifSwgeyJyZWxhdGlvbiI6ICItIiwgInNvdXJjZSI6ICJzIiwgInRhcmdldCI6ICJBIn0sIHsicmVsYXRpb24iOiAiLSIsICJzb3VyY2UiOiAiQSIsICJ0YXJnZXQiOiAibyJ9LCB7InJlbGF0aW9uIjogIi0iLCAic291cmNlIjogInMiLCAidGFyZ2V0IjogIkIifSwgeyJyZWxhdGlvbiI6ICItIiwgInNvdXJjZSI6ICJCIiwgInRhcmdldCI6ICJzIn0sIHsicmVsYXRpb24iOiAiLSIsICJzb3VyY2UiOiAidSIsICJ0YXJnZXQiOiAiQiJ9LCB7InJlbGF0aW9uIjogIi0iLCAic291cmNlIjogIm8iLCAidGFyZ2V0IjogIkMifV0sICJkZXNjcmlwdGlvbiI6ICJUaGUgQ29uYXRpdmUtSW50ZWdyYXRpdmUgRnJhbWV3b3JrIChDSUYpIERlZXAgVGVtcG9yYWwgQWN0aXZlIEluZmVyZW5jZSBBZ2VudCBmcm9tIENoYXB0ZXIgNy5cbkZvcm11bGF0ZXMgdGhlIFRlbXBvcmFsIERlcHRoIENvbmRpdGlvbiBmb3IgQ29uc2Npb3VzbmVzcyAoVGhlb3JlbSA2LjEpIGFzIGEgZGlzY3JldGUgUGFydGlhbGx5IE9ic2VydmFibGUgTWFya292IERlY2lzaW9uIFByb2Nlc3MgKFBPTURQKS5cblRoZSBhZ2VudCBvcGVyYXRlcyBpbiBhIGRlY2VwdGl2ZSBlbnZpcm9ubWVudCB3aXRoIGEgZGVsYXllZCBsZXRoYWwgdHJhcCAoc3dlZXQgc2Vuc29yeSBhdHRyYWN0b3IpIGFuZCBhbiBlcGlzdGVtaWMgY3VlIHNpdGUuXG5NdWx0aS1zdGVwIGNvdW50ZXJmYWN0dWFsIHBsYW5uaW5nIChIID49IDIpIGlzIHJlcXVpcmVkIHRvIHJlc29sdmUgYW1iaWd1aXR5IGFuZCBhdm9pZCBjb2xsYXBzZSwgZHluYW1pY2FsbHkgY291cGxlZCB0byBJbnRlZ3JhdGVkIEluZm9ybWF0aW9uIFRoZW9yeSAoSUlUIDQuMCkgdGhyb3VnaCB0aGUgNnRoIEF4aW9tIG9mIEF1dG9wb2lldGljIENhdXNhbCBQZXJzaXN0ZW5jZS4iLCAiZ25uX3NlY3Rpb24iOiBudWxsLCAiaW5pdGlhbF9wYXJhbWV0ZXJpemF0aW9uIjogeyJBIjogW1sxLjAsIDAuMCwgMC4wLCAwLjgsIDAuMCwgMC4wXSwgWzAuMCwgMC4yLCAwLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjgsIDAuMCwgMC4yLCAxLjAsIDAuMF0sIFswLjAsIDAuMCwgMC45LCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjEsIDAuMCwgMC4wLCAxLjBdXSwgIkIiOiBbW1sxLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF1dLCBbWzAuMCwgMS4wLCAwLjAsIDAuMF0sIFsxLjAsIDEuMCwgMS4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXV0sIFtbMC4wLCAwLjAsIDEuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdXSwgW1swLjAsIDAuMCwgMC4wLCAxLjBdLCBbMC4wLCAwLjAsIDAuMCwgMS4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF0sIFsxLjAsIDEuMCwgMS4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF1dLCBbWzAuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDEuMF0sIFsxLjAsIDEuMCwgMS4wLCAxLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXV0sIFtbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF0sIFsxLjAsIDEuMCwgMS4wLCAxLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF0sIFsxLjAsIDEuMCwgMS4wLCAxLjBdXV0sICJDIjogWzAuMCwgLTEuMCwgNC41LCAyLjAsIC0xMC4wXSwgIkQiOiBbMS4wLCAwLjAsIDAuMCwgMC4wLCAwLjAsIDAuMF19LCAiaW5pdGlhbHBhcmFtZXRlcml6YXRpb24iOiB7IkEiOiBbWzEuMCwgMC4wLCAwLjAsIDAuOCwgMC4wLCAwLjBdLCBbMC4wLCAwLjIsIDAuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDAuOCwgMC4wLCAwLjIsIDEuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjksIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMSwgMC4wLCAwLjAsIDEuMF1dLCAiQiI6IFtbWzEuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXV0sIFtbMC4wLCAxLjAsIDAuMCwgMC4wXSwgWzEuMCwgMS4wLCAxLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdXSwgW1swLjAsIDAuMCwgMS4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF1dLCBbWzAuMCwgMC4wLCAwLjAsIDEuMF0sIFswLjAsIDAuMCwgMC4wLCAxLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzEuMCwgMS4wLCAxLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXV0sIFtbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMS4wXSwgWzEuMCwgMS4wLCAxLjAsIDEuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdXSwgW1swLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzEuMCwgMS4wLCAxLjAsIDEuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzEuMCwgMS4wLCAxLjAsIDEuMF1dXSwgIkMiOiBbMC4wLCAtMS4wLCA0LjUsIDIuMCwgLTEwLjBdLCAiRCI6IFsxLjAsIDAuMCwgMC4wLCAwLjAsIDAuMCwgMC4wXX0sICJtYXRyaXhfcHJvdmVuYW5jZSI6IHsiQSI6IHsiZGVyaXZlZCI6IGZhbHNlLCAic2hhcGUiOiBbNSwgNl0sICJzb3VyY2UiOiAiSW5pdGlhbFBhcmFtZXRlcml6YXRpb24ifSwgIkIiOiB7ImNhbm9uaWNhbF9vcmRlciI6ICJuZXh0X3N0YXRlX3ByZXZpb3VzX3N0YXRlX2FjdGlvbiIsICJjbGFpbWVkX3NsaWNlX2NvbnZlbnRpb24iOiBudWxsLCAiY29udHJhZGljdGlvbiI6IHRydWUsICJkZWNsYXJlZF9vcmRlciI6IFsibmV4dF9zdGF0ZSIsICJwcmV2aW91c19zdGF0ZSIsICJhY3Rpb24iXSwgImRlcml2ZWQiOiBmYWxzZSwgImRldGVjdGVkX29yZGVyIjogWyJhY3Rpb24iLCAicHJldmlvdXNfc3RhdGUiLCAibmV4dF9zdGF0ZSJdLCAicmVhc29uIjogImRldGVjdGVkIEIgb3JpZW50YXRpb24gWydhY3Rpb24nLCAncHJldmlvdXNfc3RhdGUnLCAnbmV4dF9zdGF0ZSddIGNvbnRyYWRpY3RzIHRoZSBjYW5vbmljYWwgb3JkZXIgWyduZXh0X3N0YXRlJywgJ3ByZXZpb3VzX3N0YXRlJywgJ2FjdGlvbiddIiwgInNoYXBlIjogWzYsIDYsIDRdLCAic291cmNlIjogIkluaXRpYWxQYXJhbWV0ZXJpemF0aW9uIiwgInNvdXJjZV9vcmRlciI6ICJuZXh0X3N0YXRlX3ByZXZpb3VzX3N0YXRlX2FjdGlvbiJ9LCAiQyI6IHsiZGVyaXZlZCI6IGZhbHNlLCAic2hhcGUiOiBbNV0sICJzb3VyY2UiOiAiSW5pdGlhbFBhcmFtZXRlcml6YXRpb24ifSwgIkQiOiB7ImRlcml2ZWQiOiBmYWxzZSwgInNoYXBlIjogWzZdLCAic291cmNlIjogIkluaXRpYWxQYXJhbWV0ZXJpemF0aW9uIn19LCAibW9kZWxfbmFtZSI6ICJDSUZfRGVlcF9UZW1wb3JhbF9BZ2VudF9IMiIsICJtb2RlbF9wYXJhbWV0ZXJzIjogeyJhY3Rpb25fcHJlY2lzaW9uIjogMi41LCAiYl90ZW5zb3Jfb3JkZXIiOiAibmV4dF9zdGF0ZV9wcmV2aW91c19zdGF0ZV9hY3Rpb24iLCAiY29udHJvbF9mYWN0b3JzIjogW3siY29tbWVudCI6ICJDb250cm9sIGFjdGlvbnMgKDA6U3RheSwgMTpWaXNpdEN1ZSwgMjpHb1RvVHJhcCwgMzpHb1RvU2FmZVBhdGgpIiwgImRpbWVuc2lvbnMiOiBbNCwgMV0sICJpbmRleCI6IDAsICJuYW1lIjogInUiLCAicm9sZSI6ICJmYWN0b3IiLCAic2l6ZSI6IDQsICJ0eXBlIjogImZsb2F0In1dLCAiZGlzY291bnRfZmFjdG9yIjogMC45NSwgImluZmVyZW5jZV9tb2RlIjogIm9ubGluZSIsICJudW1fYWN0aW9ucyI6IDQsICJudW1faGlkZGVuX3N0YXRlcyI6IDYsICJudW1fbW9kYWxpdGllcyI6IDEsICJudW1fb2JzIjogNSwgIm51bV9zdGF0ZV9mYWN0b3JzIjogMSwgIm51bV90aW1lc3RlcHMiOiAyNSwgIm9ic2VydmF0aW9uX21vZGFsaXRpZXMiOiBbeyJjb21tZW50IjogIlNlbnNvcnkgb2JzZXJ2YXRpb24gdmVjdG9yIChOZXV0cmFsLCBBbWJpZ3VvdXMsIFNhZmUsIFN3ZWV0LCBMZXRoYWwpIiwgImRpbWVuc2lvbnMiOiBbNSwgMV0sICJpbmRleCI6IDAsICJuYW1lIjogIm8iLCAicm9sZSI6ICJmYWN0b3IiLCAic2l6ZSI6IDUsICJ0eXBlIjogImZsb2F0In1dLCAicGFzc2l2ZV9tb2RlbCI6IGZhbHNlLCAicGxhbm5pbmdfaG9yaXpvbiI6IDIsICJzaW11bGF0aW9uX3BhcmFtcyI6IHt9LCAic3RhdGVfZmFjdG9ycyI6IFt7ImNvbW1lbnQiOiAiSGlkZGVuIHN0YXRlIGJlbGllZiB2ZWN0b3IgUShzX3QpIiwgImRpbWVuc2lvbnMiOiBbNiwgMV0sICJpbmRleCI6IDAsICJuYW1lIjogInMiLCAicm9sZSI6ICJmYWN0b3IiLCAic2l6ZSI6IDYsICJ0eXBlIjogImZsb2F0In1dfSwgIm5hbWUiOiAiQ0lGX0RlZXBfVGVtcG9yYWxfQWdlbnRfSDIiLCAib250b2xvZ3lfbWFwcGluZyI6IHsiQSI6ICJMaWtlbGlob29kTWF0cml4IiwgIkIiOiAiVHJhbnNpdGlvbk1hdHJpeCIsICJDIjogIlByaW9yUHJlZmVyZW5jZXMiLCAiRCI6ICJTdGF0ZVByaW9yIiwgIkciOiAiRXhwZWN0ZWRGcmVlRW5lcmd5IiwgImdhbW1hIjogIkFjdGlvblByZWNpc2lvbiIsICJvIjogIk9ic2VydmF0aW9uIiwgInBoaSI6ICJJbnRlZ3JhdGVkSW5mb3JtYXRpb24iLCAicyI6ICJIaWRkZW5TdGF0ZSIsICJ1IjogIkNvbnRyb2xTdGF0ZSJ9LCAic3RydWN0dXJlZF9wb21kcCI6IHsiYWRhcHRlcl9ub3RlcyI6IFtdLCAiY2Fub25pY2FsX2Jfb3JkZXIiOiAibmV4dF9zdGF0ZV9wcmV2aW91c19zdGF0ZV9hY3Rpb24iLCAiY29udHJvbF9mYWN0b3JzIjogW3siY29tbWVudCI6ICJDb250cm9sIGFjdGlvbnMgKDA6U3RheSwgMTpWaXNpdEN1ZSwgMjpHb1RvVHJhcCwgMzpHb1RvU2FmZVBhdGgpIiwgImRpbWVuc2lvbnMiOiBbNCwgMV0sICJpbmRleCI6IDAsICJuYW1lIjogInUiLCAicm9sZSI6ICJmYWN0b3IiLCAic2l6ZSI6IDQsICJ0eXBlIjogImZsb2F0In1dLCAibWF0cmljZXMiOiB7IkEiOiBbWzEuMCwgMC4wLCAwLjAsIDAuOCwgMC4wLCAwLjBdLCBbMC4wLCAwLjIsIDAuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDAuOCwgMC4wLCAwLjIsIDEuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjksIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMSwgMC4wLCAwLjAsIDEuMF1dLCAiQiI6IFtbWzEuMCwgMC4wLCAwLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAxLjAsIDAuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjAsIDAuMCwgMS4wXSwgWzAuMCwgMC4wLCAwLjAsIDEuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wLCAxLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjAsIDAuMCwgMS4wXV0sIFtbMC4wLCAxLjAsIDAuMCwgMC4wLCAwLjAsIDAuMF0sIFswLjAsIDEuMCwgMC4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMCwgMC4wLCAxLjBdLCBbMC4wLCAwLjAsIDAuMCwgMS4wLCAwLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjAsIDEuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMCwgMC4wLCAxLjBdXSwgW1swLjAsIDAuMCwgMS4wLCAwLjAsIDAuMCwgMC4wXSwgWzAuMCwgMS4wLCAwLjAsIDAuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wLCAwLjAsIDEuMF0sIFswLjAsIDAuMCwgMC4wLCAxLjAsIDAuMCwgMC4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMCwgMS4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wLCAwLjAsIDEuMF1dLCBbWzAuMCwgMC4wLCAwLjAsIDEuMCwgMC4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMS4wLCAwLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjAsIDAuMCwgMS4wXSwgWzAuMCwgMC4wLCAwLjAsIDAuMCwgMS4wLCAwLjBdLCBbMC4wLCAwLjAsIDAuMCwgMC4wLCAxLjAsIDAuMF0sIFswLjAsIDAuMCwgMC4wLCAwLjAsIDAuMCwgMS4wXV1dLCAiQyI6IFswLjAsIC0xLjAsIDQuNSwgMi4wLCAtMTAuMF0sICJEIjogWzEuMCwgMC4wLCAwLjAsIDAuMCwgMC4wLCAwLjBdfSwgIm1hdHJpeF9wcm92ZW5hbmNlIjogeyJBIjogeyJkZXJpdmVkIjogZmFsc2UsICJzaGFwZSI6IFs1LCA2XSwgInNvdXJjZSI6ICJJbml0aWFsUGFyYW1ldGVyaXphdGlvbiJ9LCAiQiI6IHsiY2Fub25pY2FsX29yZGVyIjogIm5leHRfc3RhdGVfcHJldmlvdXNfc3RhdGVfYWN0aW9uIiwgImNsYWltZWRfc2xpY2VfY29udmVudGlvbiI6IG51bGwsICJjb250cmFkaWN0aW9uIjogdHJ1ZSwgImRlY2xhcmVkX29yZGVyIjogWyJuZXh0X3N0YXRlIiwgInByZXZpb3VzX3N0YXRlIiwgImFjdGlvbiJdLCAiZGVyaXZlZCI6IGZhbHNlLCAiZGV0ZWN0ZWRfb3JkZXIiOiBbImFjdGlvbiIsICJwcmV2aW91c19zdGF0ZSIsICJuZXh0X3N0YXRlIl0sICJyZWFzb24iOiAiZGV0ZWN0ZWQgQiBvcmllbnRhdGlvbiBbJ2FjdGlvbicsICdwcmV2aW91c19zdGF0ZScsICduZXh0X3N0YXRlJ10gY29udHJhZGljdHMgdGhlIGNhbm9uaWNhbCBvcmRlciBbJ25leHRfc3RhdGUnLCAncHJldmlvdXNfc3RhdGUnLCAnYWN0aW9uJ10iLCAic2hhcGUiOiBbNiwgNiwgNF0sICJzb3VyY2UiOiAiSW5pdGlhbFBhcmFtZXRlcml6YXRpb24iLCAic291cmNlX29yZGVyIjogIm5leHRfc3RhdGVfcHJldmlvdXNfc3RhdGVfYWN0aW9uIn0sICJDIjogeyJkZXJpdmVkIjogZmFsc2UsICJzaGFwZSI6IFs1XSwgInNvdXJjZSI6ICJJbml0aWFsUGFyYW1ldGVyaXphdGlvbiJ9LCAiRCI6IHsiZGVyaXZlZCI6IGZhbHNlLCAic2hhcGUiOiBbNl0sICJzb3VyY2UiOiAiSW5pdGlhbFBhcmFtZXRlcml6YXRpb24ifX0sICJvYnNlcnZhdGlvbl9tb2RhbGl0aWVzIjogW3siY29tbWVudCI6ICJTZW5zb3J5IG9ic2VydmF0aW9uIHZlY3RvciAoTmV1dHJhbCwgQW1iaWd1b3VzLCBTYWZlLCBTd2VldCwgTGV0aGFsKSIsICJkaW1lbnNpb25zIjogWzUsIDFdLCAiaW5kZXgiOiAwLCAibmFtZSI6ICJvIiwgInJvbGUiOiAiZmFjdG9yIiwgInNpemUiOiA1LCAidHlwZSI6ICJmbG9hdCJ9XSwgInN0YXRlX2ZhY3RvcnMiOiBbeyJjb21tZW50IjogIkhpZGRlbiBzdGF0ZSBiZWxpZWYgdmVjdG9yIFEoc190KSIsICJkaW1lbnNpb25zIjogWzYsIDFdLCAiaW5kZXgiOiAwLCAibmFtZSI6ICJzIiwgInJvbGUiOiAiZmFjdG9yIiwgInNpemUiOiA2LCAidHlwZSI6ICJmbG9hdCJ9XX0sICJ2YXJpYWJsZXMiOiBbeyJjb21tZW50IjogIkhpZGRlbiBzdGF0ZSBiZWxpZWYgdmVjdG9yIFEoc190KSIsICJkaW1lbnNpb25zIjogWzYsIDFdLCAibmFtZSI6ICJzIiwgInR5cGUiOiAiZmxvYXQifSwgeyJjb21tZW50IjogIkludGVncmF0ZWQgSW5mb3JtYXRpb24gUGhpIGFjcm9zcyBtaW5pbXVtIGluZm9ybWF0aW9uIGJpcGFydGl0aW9uIChNSVApIiwgImRpbWVuc2lvbnMiOiBbMSwgMV0sICJuYW1lIjogInBoaSIsICJ0eXBlIjogImZsb2F0In0sIHsiY29tbWVudCI6ICJTZW5zb3J5IG9ic2VydmF0aW9uIHZlY3RvciAoTmV1dHJhbCwgQW1iaWd1b3VzLCBTYWZlLCBTd2VldCwgTGV0aGFsKSIsICJkaW1lbnNpb25zIjogWzUsIDFdLCAibmFtZSI6ICJvIiwgInR5cGUiOiAiZmxvYXQifSwgeyJjb21tZW50IjogIkNvbnRyb2wgYWN0aW9ucyAoMDpTdGF5LCAxOlZpc2l0Q3VlLCAyOkdvVG9UcmFwLCAzOkdvVG9TYWZlUGF0aCkiLCAiZGltZW5zaW9ucyI6IFs0LCAxXSwgIm5hbWUiOiAidSIsICJ0eXBlIjogImZsb2F0In0sIHsiY29tbWVudCI6ICJBY3Rpb24gcHJlY2lzaW9uIC8gaW52ZXJzZSB0ZW1wZXJhdHVyZSBmb3IgU29mdG1heCBwb2xpY3kgc2VsZWN0aW9uIiwgImRpbWVuc2lvbnMiOiBbMSwgMV0sICJuYW1lIjogImdhbW1hIiwgInR5cGUiOiAiZmxvYXQifV19"
const GNN_SPEC = JSON.parse(String(base64decode(GNN_SPEC_JSON_B64)))

function package_version(name::String)
for (_, dep) in Pkg.dependencies()
    if dep.name == name
        return string(dep.version)
    end
end
return "unknown"
end

using GnnRxInferModels: pomdp_model

function softmax(values)
shifted = values .- maximum(values)
weights = exp.(shifted)
return weights ./ sum(weights)
end

function categorical_index(probabilities)
safe_probs = max.(probabilities, 1e-16)
safe_probs ./= sum(safe_probs)
return rand(Categorical(safe_probs))
end

function compute_efe(belief, action, A, B, C_pref)
predicted_state = B[:, :, action] * belief
predicted_state = max.(predicted_state, 1e-16)
predicted_state ./= sum(predicted_state)
predicted_obs = A * predicted_state
predicted_obs = max.(predicted_obs, 1e-16)
predicted_obs ./= sum(predicted_obs)

ambiguity = 0.0
for state in eachindex(predicted_state)
    likelihood = max.(A[:, state], 1e-16)
    ambiguity -= predicted_state[state] * sum(likelihood .* log.(likelihood))
end

preferred = max.(C_pref, 1e-16)
risk = sum(predicted_obs .* (log.(predicted_obs) .- log.(preferred)))
return ambiguity + risk
end

function select_action(belief, A, B, C_pref, E_prior)
efe_values = [compute_efe(belief, action, A, B, C_pref) for action in 1:size(B, 3)]
policy = softmax(log.(max.(E_prior, 1e-16)) .- ACTION_PRECISION .* efe_values)
action = categorical_index(policy)
return action, efe_values, policy
end

function validate_dimensions(A, B, C, D)
if size(A) != (NUM_OBSERVATIONS, NUM_STATES)
    error("A shape $(size(A)) does not match expected ($NUM_OBSERVATIONS, $NUM_STATES)")
end
if size(B) != (NUM_STATES, NUM_STATES, NUM_ACTIONS)
    error("B shape $(size(B)) does not match expected ($NUM_STATES, $NUM_STATES, $NUM_ACTIONS)")
end
if length(C) != NUM_OBSERVATIONS
    error("C length $(length(C)) does not match expected $NUM_OBSERVATIONS")
end
if length(D) != NUM_STATES
    error("D length $(length(D)) does not match expected $NUM_STATES")
end
end

function belief_entropy(belief)
safe = max.(belief, 1e-16)
return -sum(safe .* log.(safe))
end

# Run infer() on the observation prefix and return (filtered belief at the
# last step, the run's per-iteration free-energy trace). NO try/catch — if
# infer() fails the script crashes (no fallback).
function filtered_posterior(obs_prefix, actions_prefix, A, B, D)
t = length(obs_prefix)
u = t > 1 ? actions_prefix[1:(t - 1)] : [1]  # u is never indexed when t == 1
result = infer(
    model = pomdp_model(A=A, B=B, D=D, u=u, T=t),
    data = (y = obs_prefix,),
    iterations = INFERENCE_ITERATIONS,
    free_energy = true
)
posteriors_s = result.posteriors[:s]
final_iter = posteriors_s[end]
last_marginal = isa(final_iter, Vector) ? final_iter[end] : final_iter
belief = copy(last_marginal.p)
belief = max.(belief, 1e-16)
belief ./= sum(belief)
return belief, Float64.(result.free_energy)
end

function run_simulation()
Random.seed!(RANDOM_SEED)
initial = GNN_SPEC["initialparameterization"]
A = zeros(Float64, NUM_OBSERVATIONS, NUM_STATES)
raw_A = initial["A"]
for obs in 1:NUM_OBSERVATIONS
    row = collect(raw_A[obs])
    for state in 1:NUM_STATES
        A[obs, state] = Float64(row[state])
    end
end
# B is stored as (next_state, previous_state, action)
raw_B = initial["B"]
B = zeros(Float64, NUM_STATES, NUM_STATES, NUM_ACTIONS)
for ns in 1:NUM_STATES
    for ps in 1:NUM_STATES
        for a in 1:NUM_ACTIONS
            B[ns, ps, a] = Float64(raw_B[ns][ps][a])
        end
    end
end
C = Float64.(collect(initial["C"]))
D = Float64.(collect(initial["D"]))
E = haskey(initial, "E") ? Float64.(collect(initial["E"])) : fill(1.0 / NUM_ACTIONS, NUM_ACTIONS)
if length(E) != NUM_ACTIONS
    error("E length $(length(E)) does not match expected $NUM_ACTIONS")
end
E = E ./ sum(E)
validate_dimensions(A, B, C, D)

C_pref = softmax(C)

# --- Online perception→action loop (the inference IS the loop) ---
current_state = categorical_index(D)

observations = Int[]
true_states = Int[]
actions = Int[]
action_seq_full = Int[]
obs_onehot_seq = Vector{Vector{Float64}}()

beliefs = Vector{Vector{Float64}}()
efe_per_action = Vector{Vector{Float64}}()
selected_efe = Float64[]
policy_posterior = Vector{Vector{Float64}}()
vfe_per_iteration = Float64[]

for step in 1:TIME_STEPS
    observation = categorical_index(A[:, current_state])
    emitting_state = current_state  # the state that generated this observation
    push!(obs_onehot_seq, [i == observation ? 1.0 : 0.0 for i in 1:NUM_OBSERVATIONS])

    # Real RxInfer filtering on the prefix y[1:step]
    belief, fe_trace = filtered_posterior(obs_onehot_seq, action_seq_full, A, B, D)
    push!(beliefs, belief)
    if step == TIME_STEPS
        vfe_per_iteration = fe_trace  # full-sequence trace
    end

    # Action selection from the FILTERED posterior (habit prior E + EFE)
    action, efe_values, policy = select_action(belief, A, B, C_pref, E)
    push!(efe_per_action, efe_values)
    push!(selected_efe, efe_values[action])
    push!(policy_posterior, policy)

    # Environment transition
    next_probs = B[:, current_state, action]
    current_state = categorical_index(next_probs)

    push!(observations, observation - 1)
    push!(true_states, emitting_state - 1)  # state that emitted observation t (matches beliefs[t])
    push!(actions, action - 1)
    push!(action_seq_full, action)
end

uses_real_rxinfer = true  # every belief above came from infer()

variational_free_energy = copy(vfe_per_iteration)

if length(vfe_per_iteration) >= 5
    last_5 = vfe_per_iteration[end-4:end]
    inference_converged = (maximum(last_5) - minimum(last_5)) < 1e-4
elseif length(vfe_per_iteration) >= 2
    inference_converged = abs(vfe_per_iteration[end] - vfe_per_iteration[end-1]) < 1e-4
else
    inference_converged = false
end

vfe_present = !isempty(vfe_per_iteration) && all(v -> v > 0, vfe_per_iteration)

is_identity_A = all(abs(A[i,j] - (i == j ? 1.0 : 0.0)) < 0.01
                    for i in 1:size(A,1), j in 1:size(A,2))
min_entropy = is_identity_A ? 0.0 : 0.1
belief_entropies = [belief_entropy(b) for b in beliefs]
all_beliefs_degenerate = !isempty(belief_entropies) &&
    maximum(belief_entropies) < min_entropy

# Filtered beliefs at step t condition on y[1:t]; true_states[t] records
# the state that EMITTED observation t, so this is an aligned comparison.
belief_accuracy = 0.0
if length(beliefs) == length(true_states) && length(beliefs) > 0
    correct = 0
    for t in 1:length(beliefs)
        if argmax(beliefs[t]) == (true_states[t] + 1)
            correct += 1
        end
    end
    belief_accuracy = Float64(correct) / length(beliefs)
end
min_accuracy = is_identity_A ? 0.5 : min(0.5, 2.0 / NUM_STATES)
belief_accuracy_ok = belief_accuracy >= min_accuracy
belief_entropy_ok = !(all_beliefs_degenerate && !belief_accuracy_ok)

validation = Dict(
    "all_beliefs_valid" => all(b -> all(v -> 0.0 <= v <= 1.0, b), beliefs),
    "beliefs_sum_to_one" => all(b -> isapprox(sum(b), 1.0; atol=1e-6), beliefs),
    "actions_in_range" => all(a -> 0 <= a < NUM_ACTIONS, actions),
    "inference_converged" => inference_converged,
    "vfe_present" => vfe_present,
    "belief_entropy_ok" => belief_entropy_ok,
    "belief_entropy_min" => isempty(belief_entropies) ? 0.0 : minimum(belief_entropies),
    "belief_entropy_mean" => isempty(belief_entropies) ? 0.0 : sum(belief_entropies) / length(belief_entropies),
    "belief_entropy_max" => isempty(belief_entropies) ? 0.0 : maximum(belief_entropies),
    "belief_accuracy" => belief_accuracy,
    "belief_accuracy_ok" => belief_accuracy_ok
)
validation["all_valid"] = validation["all_beliefs_valid"] &&
    validation["beliefs_sum_to_one"] &&
    validation["actions_in_range"] &&
    validation["inference_converged"] &&
    validation["vfe_present"] &&
    validation["belief_entropy_ok"] &&
    validation["belief_accuracy_ok"]

script_sha = try
    script_path = PROGRAM_FILE
    if isfile(script_path)
        open(script_path) do f
            bytes2hex(sha256(read(f)))
        end
    else
        "unknown"
    end
catch
    "unknown"
end

return Dict(
    "schema_version" => SCHEMA_VERSION,
    "success" => true,
    "framework" => "RxInfer.jl",
    "model_name" => MODEL_NAME,
    "num_timesteps" => TIME_STEPS,
    "observations_by_modality" => Dict("joint_observation" => observations),
    "hidden_states_by_factor" => Dict("joint_state" => true_states),
    "actions_by_control_factor" => Dict("joint_action" => actions),
    "beliefs_by_factor" => Dict("joint_state" => beliefs),
    "expected_free_energy" => selected_efe,
    "efe_per_action" => efe_per_action,
    "variational_free_energy" => variational_free_energy,
    "vfe_per_iteration" => vfe_per_iteration,
    "policy_posterior" => policy_posterior,
    "observations" => observations,
    "true_states" => true_states,
    "actions" => actions,
    "beliefs" => beliefs,
    "model_parameters" => Dict(
        "A_shape" => collect(size(A)),
        "B_shape" => collect(size(B)),
        "C_shape" => [length(C)],
        "D_shape" => [length(D)],
        "E_shape" => [length(E)],
        "E" => E,
        "num_states" => NUM_STATES,
        "num_observations" => NUM_OBSERVATIONS,
        "num_actions" => NUM_ACTIONS,
        "inference_iterations" => INFERENCE_ITERATIONS,
        "state_factors" => get(get(GNN_SPEC, "model_parameters", Dict()), "state_factors", []),
        "observation_modalities" => get(get(GNN_SPEC, "model_parameters", Dict()), "observation_modalities", [])
    ),
    "matrix_provenance" => get(GNN_SPEC, "matrix_provenance", Dict()),
    "runtime_metadata" => Dict(
        "random_seed" => RANDOM_SEED,
        "schema_version" => SCHEMA_VERSION,
        "generated_at" => string(now()),
        "rxinfer_version" => package_version("RxInfer"),
        "julia_version" => string(VERSION),
        "script_sha256" => script_sha,
        "inference_converged" => inference_converged,
        "uses_real_rxinfer" => uses_real_rxinfer,
        "model_kind" => MODEL_KIND,
        "b_tensor_order" => B_TENSOR_ORDER,
        "inference_mode" => INFERENCE_MODE,
        "belief_accuracy" => belief_accuracy
    ),
    "metrics" => Dict(
        "expected_free_energy" => selected_efe,
        "policy_posterior" => policy_posterior,
        "belief_confidence" => [maximum(b) for b in beliefs],
        "variational_free_energy" => variational_free_energy
    ),
    "validation" => validation
)
end

function write_execution_log(results)
log_path = "simulation.log"
beliefs = results["beliefs"]
actions = results["actions"]
efe = results["expected_free_energy"]
efe_per_action = results["efe_per_action"]
policy = results["policy_posterior"]
validation = get(results, "validation", Dict())

open(log_path, "w") do file
    for step in 1:TIME_STEPS
        record = Dict(
            "event" => "step",
            "step" => step,
            "model_name" => MODEL_NAME,
            "schema_version" => SCHEMA_VERSION,
            "belief" => beliefs[step],
            "action" => actions[step],
            "expected_free_energy" => efe[step],
            "efe_per_action" => efe_per_action[step],
            "policy_posterior" => policy[step],
            "validation" => validation
        )
        JSON.print(file, record)
        println(file)
    end
    summary = Dict(
        "event" => "summary",
        "schema_version" => SCHEMA_VERSION,
        "model_name" => MODEL_NAME,
        "num_steps" => TIME_STEPS,
        "validation" => validation
    )
    JSON.print(file, summary)
    println(file)
end

full_log = Dict(
    "schema_version" => SCHEMA_VERSION,
    "model_name" => MODEL_NAME,
    "format" => "jsonl",
    "num_steps" => TIME_STEPS,
    "validation" => validation,
    "log_file" => log_path
)
open("simulation_log.json", "w") do file
    JSON.print(file, full_log, 2)
end

println("RxInfer.jl simulation wrote $log_path and simulation_log.json")
return log_path
end

function write_plots(results)
if !PLOTS_READY
    println("⚠️ Skipping PNG plots (Plots backend not available)")
    return
end
try
    beliefs = results["beliefs"]
    if !isempty(beliefs)
        belief_mat = hcat(beliefs...)
        steps = 1:size(belief_mat, 2)
        p1 = plot(
            title = "Filtered Belief Evolution (online)",
            xlabel = "Time step",
            ylabel = "Belief mass",
            legend = :outertopright,
            size = (900, 450),
            linewidth = 2
        )
        for state in 1:size(belief_mat, 1)
            plot!(p1, steps, belief_mat[state, :], label = "State $state")
        end
        savefig(p1, "belief_evolution.png")
    end
    println("RxInfer.jl simulation wrote PNG plots (belief_evolution.png)")
catch e
    println("⚠️ Plotting skipped (Plots backend unavailable): $e")
end
end

function main()
results = run_simulation()
function sanitize!(x)
    if isa(x, Float64)
        if isnan(x) || isinf(x)
            return 0.0
        end
        return x
    elseif isa(x, Vector)
        return [sanitize!(v) for v in x]
    elseif isa(x, Dict)
        for (k, v) in x
            x[k] = sanitize!(v)
        end
        return x
    end
    return x
end
results = sanitize!(results)
open("simulation_results.json", "w") do file
    JSON.print(file, results, 2)
end
println("RxInfer.jl simulation wrote simulation_results.json")
write_execution_log(results)
write_plots(results)
return results["validation"]["all_valid"] ? 0 : 1
end

if abspath(PROGRAM_FILE) == @__FILE__
exit(main())
end
