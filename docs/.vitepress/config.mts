import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
    lang: 'zh-CN',
    title: "DicerGirl",
    description: "新一代跨平台开源 TRPG 骰娘框架",

    themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        nav: [
            {
                text: '概览',
                link: '/overview/',
            },
            {
                text: '开始',
                link: '/getting-started/',
            },
            {
                text: '指南',
                link: '/usage/',
            },
        ],

        sidebar: [
            {
                text: '概览',
                link: '/overview/',
            },
            {
                text: '开始',
                link: '/getting-started/',
                items: [
                    {
                        text: '安装',
                        link: '/getting-started/installation.html',
                    },
                    {
                        text: '部署',
                        link: '/getting-started/deployment.html',
                    },
                    {
                        text: '使用',
                        link: '/getting-started/using-dicergirl.html',
                    },
                ]
            },
            {
                text: '指南',
                link: '/usage/',
                items: [
                    {
                        text: '指令',
                        link: '/usage/commands/',
                        items: [
                            {
                                text: '管理指令',
                                link: '/usage/commands/manage.html',
                            },
                            {
                                text: '内置指令',
                                link: '/usage/commands/builtins.html',
                            },
                            {
                                text: '插件指令',
                                link: '/usage/commands/plugins.html',
                            },
                        ]
                    },
                ]
            },
        ],

        docFooter: {
            prev: '上一页',
            next: '下一页'
        },
        lightModeSwitchTitle: '切换到日光模式',
        darkModeSwitchTitle: '切换到黑暗模式',
        sidebarMenuLabel: '目录',
        returnToTopLabel: '返回顶部',
        outline: {
            label: "侧边栏"
        },

        editLink: {
            pattern: 'https://github.com/noctisynth/dicer/edit/master/docs/:path',
            text: '编辑此页'
        },

        socialLinks: [
            { icon: 'github', link: 'https://github.com/noctisynth/dicer/' }
        ],

        footer: {
            message: 'Released under the <a href="https://github.com/noctisynth/dicer/blob/master/LICENSE">Apache-2.0 License</a>.',
            copyright: 'Copyright © 2011-present <a href="https://github.com/noctisynth/">Noctisynth, org</a>'
        }
    }
})
