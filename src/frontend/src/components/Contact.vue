<template>
<div class="contact EN">
    <Tree :value="treenodes_EN">
        <template #url="{ node }">
            <a :href="node.data" target="_blank">{{ node.label }}</a>
            </template>
    </Tree>
</div>
<div class="contact EE">
    <Tree :value="treenodes_EE">
        <template #url="{ node }">
            <a :href="node.data" target="_blank">{{ node.label }}</a>
            </template>
    </Tree>
</div>
</template>

<script>
import {renderLanguage} from './AppHeader.vue';
export default {
  name: 'Contact',
  mounted () {
    renderLanguage(this.$store.state.languageCode);
  },
  data() {
    return {
        treenodes_EN: [
                        {
                          key: 0,
                          label: "Help develop Face-Describer",
                          children: [
                              {key: 0-0, icon: "pi pi-google", label: "E-mail: karl.magnus.laikoja@gmail.com"},
                              {key: 0-1, icon: "pi pi-github", label: "Face-Describer repository", data:"https://github.com/KarlMagnusLaikoja/face-describer", type: 'url'},
                          ]
                        },
                        {
                          key: 1,
                          label: "Learn about the methodology",
                          children: [
                              {key: 1-0, icon: "pi pi-book", label: "Thesis", data:"https://google.com", type: 'url'},
                              {key: 1-1, icon: "pi pi-code", label: "Face-Recognition module", data:"https://pypi.org/project/face-recognition/", type: 'url'},
                          ]
                        },
                        {
                          key: 2,
                          label: "Ask a question",
                          children: [
                              {key: 2-4, icon: "pi pi-eye", label: "Author: Karl-Magnus Laikoja",
                              children: [
                                {key: 2-4-4, icon: "pi pi-google", label: "E-mail: karl.magnus.laikoja@gmail.com"},
                                {key: 2-4-5, icon: "pi pi-linkedin", label: "LinkedIn", data:"https://ee.linkedin.com/in/karl-magnus-laikoja-0ba10a225", type: 'url'}
                              ]
                              },
                              {key: 2-5, icon: "pi pi-eye", label: "Tutor: Sven Aller",
                              children: [
                                {key: 2-5-4, icon: "pi pi-google", label: ""},
                                {key: 2-5-5, icon: "pi pi-linkedin", label: "", data:"", type: 'url'}
                              ]
                              }

                          ]
                        }

        ],
        treenodes_EE: [
                        {
                          key: 0,
                          label: "Aita arendada Face-Describerit",
                          children: [
                              {key: 0-0, icon: "pi pi-google", label: "E-mail: karl.magnus.laikoja@gmail.com"},
                              {key: 0-1, icon: "pi pi-github", label: "Face-Describer repositoorium", data:"https://github.com/KarlMagnusLaikoja/face-describer", type: 'url'},
                          ]
                        },
                        {
                          key: 1,
                          label: "Uuri metoodikat",
                          children: [
                              {key: 1-0, icon: "pi pi-book", label: "Lõputöö", data:"https://google.com", type: 'url'},
                              {key: 1-1, icon: "pi pi-code", label: "Face-Recognition moodul", data:"https://pypi.org/project/face-recognition/", type: 'url'},
                          ]
                        },
                        {
                          key: 2,
                          label: "Küsi küsimusi",
                          children: [
                              {key: 2-4, icon: "pi pi-eye", label: "Autor: Karl-Magnus Laikoja",
                              children: [
                                {key: 2-4-4, icon: "pi pi-google", label: "E-mail: karl.magnus.laikoja@gmail.com"},
                                {key: 2-4-5, icon: "pi pi-linkedin", label: "LinkedIn", data:"https://ee.linkedin.com/in/karl-magnus-laikoja-0ba10a225", type: 'url'}
                              ]
                              },
                              {key: 2-5, icon: "pi pi-eye", label: "Juhendaja: Sven Aller",
                              children: [
                                {key: 2-5-4, icon: "pi pi-google", label: ""},
                                {key: 2-5-5, icon: "pi pi-linkedin", label: "", data:"", type: 'url'}
                              ]
                              }

                          ]
                        }

        ]
    }
  }
}
</script>