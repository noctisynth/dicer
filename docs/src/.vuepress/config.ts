import { defaultTheme } from 'vuepress'
const { description } = require('../../package')

export default {
    title: 'DicerGirl',
    description: description,

    head: [
        ['meta', { name: 'theme-color', content: '#3eaf7c' }],
        ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
        ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }]
    ],

    theme: defaultTheme({
        repo: 'https://github.com/noctisynth/dicer',
        docsDir: 'docs',
        editLinkText: '编辑此页',
        lastUpdated: true,
        navbar: [
            {
                text: '概览',
                link: '/overview/',
            },
            {
                text: '开始',
                link: '/getting-started/',
                children: [
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
                link: '/usage',
                children: [
                    {
                        text: '指令',
                        link: '/usage/commands/',
                        children: [
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
        sidebar: [
            {
                text: '概览',
                link: '/overview/',
            },
            {
                text: '开始',
                link: '/getting-started/',
                children: [
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
                link: '/usage',
                children: [
                    {
                        text: '指令',
                        link: '/usage/commands/',
                        children: [
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
    }),

    plugins: []
}
