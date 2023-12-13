var __getOwnPropNames = Object.getOwnPropertyNames;
var __commonJS = (cb, mod) => function __require() {
  return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};

// package.json
var require_package = __commonJS({
  "package.json"(exports, module) {
    module.exports = {
      name: "dicer",
      version: "3.5.1",
      description: "DicerGirl - \u65B0\u4E00\u4EE3\u8DE8\u5E73\u53F0 TRPG \u9AB0\u5A18\u6846\u67B6",
      main: "index.js",
      authors: {
        name: "\u82CF\u5411\u591C",
        email: "fu050409@163.com"
      },
      repository: "https://github.com/noctisynth/dicer/dicer",
      scripts: {
        dev: "vuepress dev src",
        build: "vuepress build src"
      },
      license: "Apache-2.0",
      devDependencies: {
        vuepress: "^2.0.0-rc.0",
        "vuepress-plugin-code-copy": "^1.0.6"
      }
    };
  }
});

// src/.vuepress/config.js
import { defaultTheme } from "vuepress";
import PluginCodeCopy from "vuepress-plugin-code-copy";
var { description } = require_package();
var config_default = {
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#title
   */
  title: "DicerGirl - \u65B0\u4E00\u4EE3\u8DE8\u5E73\u53F0 TRPG \u9AB0\u5A18\u6846\u67B6",
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#description
   */
  description,
  /**
   * Extra tags to be injected to the page HTML `<head>`
   *
   * ref：https://v1.vuepress.vuejs.org/config/#head
   */
  head: [
    ["meta", { name: "theme-color", content: "#3eaf7c" }],
    ["meta", { name: "apple-mobile-web-app-capable", content: "yes" }],
    ["meta", { name: "apple-mobile-web-app-status-bar-style", content: "black" }]
  ],
  /**
   * Theme configuration, here is the default theme configuration for VuePress.
   *
   * ref：https://v1.vuepress.vuejs.org/theme/default-theme-config.html
   */
  theme: defaultTheme({
    repo: "https://github.com/noctisynth/dicer",
    editLinks: true,
    docsDir: "docs",
    editLinkText: "\u7F16\u8F91\u6B64\u9875",
    lastUpdated: true,
    nav: [
      {
        text: "\u6982\u89C8",
        link: "/overview/"
      }
    ],
    sidebar: {
      "/overview/": [
        {
          title: "\u6982\u89C8",
          collapsable: false,
          children: []
        }
      ]
    },
    nextLinks: true,
    prevLinks: true
  }),
  /**
   * Apply plugins，ref：https://v1.vuepress.vuejs.org/zh/plugin/
   */
  plugins: [
    // '@vuepress/plugin-back-to-top',
    // '@vuepress/plugin-medium-zoom',
    PluginCodeCopy()
  ]
};
export {
  config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsicGFja2FnZS5qc29uIiwgInNyYy8udnVlcHJlc3MvY29uZmlnLmpzIl0sCiAgInNvdXJjZXNDb250ZW50IjogWyJ7XHJcbiAgXCJuYW1lXCI6IFwiZGljZXJcIixcclxuICBcInZlcnNpb25cIjogXCIzLjUuMVwiLFxyXG4gIFwiZGVzY3JpcHRpb25cIjogXCJEaWNlckdpcmwgLSBcdTY1QjBcdTRFMDBcdTRFRTNcdThERThcdTVFNzNcdTUzRjAgVFJQRyBcdTlBQjBcdTVBMThcdTY4NDZcdTY3QjZcIixcclxuICBcIm1haW5cIjogXCJpbmRleC5qc1wiLFxyXG4gIFwiYXV0aG9yc1wiOiB7XHJcbiAgICBcIm5hbWVcIjogXCJcdTgyQ0ZcdTU0MTFcdTU5MUNcIixcclxuICAgIFwiZW1haWxcIjogXCJmdTA1MDQwOUAxNjMuY29tXCJcclxuICB9LFxyXG4gIFwicmVwb3NpdG9yeVwiOiBcImh0dHBzOi8vZ2l0aHViLmNvbS9ub2N0aXN5bnRoL2RpY2VyL2RpY2VyXCIsXHJcbiAgXCJzY3JpcHRzXCI6IHtcclxuICAgIFwiZGV2XCI6IFwidnVlcHJlc3MgZGV2IHNyY1wiLFxyXG4gICAgXCJidWlsZFwiOiBcInZ1ZXByZXNzIGJ1aWxkIHNyY1wiXHJcbiAgfSxcclxuICBcImxpY2Vuc2VcIjogXCJBcGFjaGUtMi4wXCIsXHJcbiAgXCJkZXZEZXBlbmRlbmNpZXNcIjoge1xyXG4gICAgXCJ2dWVwcmVzc1wiOiBcIl4yLjAuMC1yYy4wXCIsXHJcbiAgICBcInZ1ZXByZXNzLXBsdWdpbi1jb2RlLWNvcHlcIjogXCJeMS4wLjZcIlxyXG4gIH1cclxufVxyXG4iLCAiY29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2Rpcm5hbWUgPSBcIkM6L1VzZXJzL2Z1MDUwL0Rlc2t0b3AvUHJvamVjdHMvRGljZXJHaXJsL2RvY3Mvc3JjLy52dWVwcmVzc1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9maWxlbmFtZSA9IFwiQzpcXFxcVXNlcnNcXFxcZnUwNTBcXFxcRGVza3RvcFxcXFxQcm9qZWN0c1xcXFxEaWNlckdpcmxcXFxcZG9jc1xcXFxzcmNcXFxcLnZ1ZXByZXNzXFxcXGNvbmZpZy5qc1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vQzovVXNlcnMvZnUwNTAvRGVza3RvcC9Qcm9qZWN0cy9EaWNlckdpcmwvZG9jcy9zcmMvLnZ1ZXByZXNzL2NvbmZpZy5qc1wiO2ltcG9ydCB7IGRlZmF1bHRUaGVtZSB9IGZyb20gJ3Z1ZXByZXNzJ1xyXG5pbXBvcnQgUGx1Z2luQ29kZUNvcHkgZnJvbSAndnVlcHJlc3MtcGx1Z2luLWNvZGUtY29weSdcclxuY29uc3QgeyBkZXNjcmlwdGlvbiB9ID0gcmVxdWlyZSgnLi4vLi4vcGFja2FnZScpXHJcblxyXG5leHBvcnQgZGVmYXVsdCB7XHJcbiAgLyoqXHJcbiAgICogUmVmXHVGRjFBaHR0cHM6Ly92MS52dWVwcmVzcy52dWVqcy5vcmcvY29uZmlnLyN0aXRsZVxyXG4gICAqL1xyXG4gIHRpdGxlOiAnRGljZXJHaXJsIC0gXHU2NUIwXHU0RTAwXHU0RUUzXHU4REU4XHU1RTczXHU1M0YwIFRSUEcgXHU5QUIwXHU1QTE4XHU2ODQ2XHU2N0I2JyxcclxuICAvKipcclxuICAgKiBSZWZcdUZGMUFodHRwczovL3YxLnZ1ZXByZXNzLnZ1ZWpzLm9yZy9jb25maWcvI2Rlc2NyaXB0aW9uXHJcbiAgICovXHJcbiAgZGVzY3JpcHRpb246IGRlc2NyaXB0aW9uLFxyXG5cclxuICAvKipcclxuICAgKiBFeHRyYSB0YWdzIHRvIGJlIGluamVjdGVkIHRvIHRoZSBwYWdlIEhUTUwgYDxoZWFkPmBcclxuICAgKlxyXG4gICAqIHJlZlx1RkYxQWh0dHBzOi8vdjEudnVlcHJlc3MudnVlanMub3JnL2NvbmZpZy8jaGVhZFxyXG4gICAqL1xyXG4gIGhlYWQ6IFtcclxuICAgIFsnbWV0YScsIHsgbmFtZTogJ3RoZW1lLWNvbG9yJywgY29udGVudDogJyMzZWFmN2MnIH1dLFxyXG4gICAgWydtZXRhJywgeyBuYW1lOiAnYXBwbGUtbW9iaWxlLXdlYi1hcHAtY2FwYWJsZScsIGNvbnRlbnQ6ICd5ZXMnIH1dLFxyXG4gICAgWydtZXRhJywgeyBuYW1lOiAnYXBwbGUtbW9iaWxlLXdlYi1hcHAtc3RhdHVzLWJhci1zdHlsZScsIGNvbnRlbnQ6ICdibGFjaycgfV1cclxuICBdLFxyXG5cclxuICAvKipcclxuICAgKiBUaGVtZSBjb25maWd1cmF0aW9uLCBoZXJlIGlzIHRoZSBkZWZhdWx0IHRoZW1lIGNvbmZpZ3VyYXRpb24gZm9yIFZ1ZVByZXNzLlxyXG4gICAqXHJcbiAgICogcmVmXHVGRjFBaHR0cHM6Ly92MS52dWVwcmVzcy52dWVqcy5vcmcvdGhlbWUvZGVmYXVsdC10aGVtZS1jb25maWcuaHRtbFxyXG4gICAqL1xyXG4gIHRoZW1lOiBkZWZhdWx0VGhlbWUoe1xyXG4gICAgcmVwbzogJ2h0dHBzOi8vZ2l0aHViLmNvbS9ub2N0aXN5bnRoL2RpY2VyJyxcclxuICAgIGVkaXRMaW5rczogdHJ1ZSxcclxuICAgIGRvY3NEaXI6ICdkb2NzJyxcclxuICAgIGVkaXRMaW5rVGV4dDogJ1x1N0YxNlx1OEY5MVx1NkI2NFx1OTg3NScsXHJcbiAgICBsYXN0VXBkYXRlZDogdHJ1ZSxcclxuICAgIG5hdjogW1xyXG4gICAgICB7XHJcbiAgICAgICAgdGV4dDogJ1x1Njk4Mlx1ODlDOCcsXHJcbiAgICAgICAgbGluazogJy9vdmVydmlldy8nLFxyXG4gICAgICB9LFxyXG4gICAgXSxcclxuICAgIHNpZGViYXI6IHtcclxuICAgICAgJy9vdmVydmlldy8nOiBbXHJcbiAgICAgICAge1xyXG4gICAgICAgICAgdGl0bGU6ICdcdTY5ODJcdTg5QzgnLFxyXG4gICAgICAgICAgY29sbGFwc2FibGU6IGZhbHNlLFxyXG4gICAgICAgICAgY2hpbGRyZW46IFtdXHJcbiAgICAgICAgfVxyXG4gICAgICBdLFxyXG4gICAgfSxcclxuICAgIG5leHRMaW5rczogdHJ1ZSxcclxuICAgIHByZXZMaW5rczogdHJ1ZVxyXG4gIH0pLFxyXG5cclxuICAvKipcclxuICAgKiBBcHBseSBwbHVnaW5zXHVGRjBDcmVmXHVGRjFBaHR0cHM6Ly92MS52dWVwcmVzcy52dWVqcy5vcmcvemgvcGx1Z2luL1xyXG4gICAqL1xyXG4gIHBsdWdpbnM6IFtcclxuICAgIC8vICdAdnVlcHJlc3MvcGx1Z2luLWJhY2stdG8tdG9wJyxcclxuICAgIC8vICdAdnVlcHJlc3MvcGx1Z2luLW1lZGl1bS16b29tJyxcclxuICAgIFBsdWdpbkNvZGVDb3B5KCksXHJcbiAgXVxyXG59XHJcbiJdLAogICJtYXBwaW5ncyI6ICI7Ozs7OztBQUFBO0FBQUE7QUFBQTtBQUFBLE1BQ0UsTUFBUTtBQUFBLE1BQ1IsU0FBVztBQUFBLE1BQ1gsYUFBZTtBQUFBLE1BQ2YsTUFBUTtBQUFBLE1BQ1IsU0FBVztBQUFBLFFBQ1QsTUFBUTtBQUFBLFFBQ1IsT0FBUztBQUFBLE1BQ1g7QUFBQSxNQUNBLFlBQWM7QUFBQSxNQUNkLFNBQVc7QUFBQSxRQUNULEtBQU87QUFBQSxRQUNQLE9BQVM7QUFBQSxNQUNYO0FBQUEsTUFDQSxTQUFXO0FBQUEsTUFDWCxpQkFBbUI7QUFBQSxRQUNqQixVQUFZO0FBQUEsUUFDWiw2QkFBNkI7QUFBQSxNQUMvQjtBQUFBLElBQ0Y7QUFBQTtBQUFBOzs7QUNuQnNXLFNBQVMsb0JBQW9CO0FBQ25ZLE9BQU8sb0JBQW9CO0FBQzNCLElBQU0sRUFBRSxZQUFZLElBQUk7QUFFeEIsSUFBTyxpQkFBUTtBQUFBO0FBQUE7QUFBQTtBQUFBLEVBSWIsT0FBTztBQUFBO0FBQUE7QUFBQTtBQUFBLEVBSVA7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUEsRUFPQSxNQUFNO0FBQUEsSUFDSixDQUFDLFFBQVEsRUFBRSxNQUFNLGVBQWUsU0FBUyxVQUFVLENBQUM7QUFBQSxJQUNwRCxDQUFDLFFBQVEsRUFBRSxNQUFNLGdDQUFnQyxTQUFTLE1BQU0sQ0FBQztBQUFBLElBQ2pFLENBQUMsUUFBUSxFQUFFLE1BQU0seUNBQXlDLFNBQVMsUUFBUSxDQUFDO0FBQUEsRUFDOUU7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUEsRUFPQSxPQUFPLGFBQWE7QUFBQSxJQUNsQixNQUFNO0FBQUEsSUFDTixXQUFXO0FBQUEsSUFDWCxTQUFTO0FBQUEsSUFDVCxjQUFjO0FBQUEsSUFDZCxhQUFhO0FBQUEsSUFDYixLQUFLO0FBQUEsTUFDSDtBQUFBLFFBQ0UsTUFBTTtBQUFBLFFBQ04sTUFBTTtBQUFBLE1BQ1I7QUFBQSxJQUNGO0FBQUEsSUFDQSxTQUFTO0FBQUEsTUFDUCxjQUFjO0FBQUEsUUFDWjtBQUFBLFVBQ0UsT0FBTztBQUFBLFVBQ1AsYUFBYTtBQUFBLFVBQ2IsVUFBVSxDQUFDO0FBQUEsUUFDYjtBQUFBLE1BQ0Y7QUFBQSxJQUNGO0FBQUEsSUFDQSxXQUFXO0FBQUEsSUFDWCxXQUFXO0FBQUEsRUFDYixDQUFDO0FBQUE7QUFBQTtBQUFBO0FBQUEsRUFLRCxTQUFTO0FBQUE7QUFBQTtBQUFBLElBR1AsZUFBZTtBQUFBLEVBQ2pCO0FBQ0Y7IiwKICAibmFtZXMiOiBbXQp9Cg==
