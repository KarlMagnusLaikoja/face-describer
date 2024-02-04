<template>
<div class="home">
    <div class="intro">
        <div class="EN">
            <h1>Create a comprehensive facial description</h1>
            <p>Facedescriber is an application created to find and describe faces within an input image via image processing and classification.</p>
            <p>It was produced as the result of the author's bachelor's thesis.</p>
        </div>
        <div class="EE">
            <h1>Loo sisukas näokirjeldus</h1>
            <p>Facedescriber on rakendus loodud sisendpildilt nägude leidmiseks ja kirjeldamiseks kasutades pilditöötlust ja klassifitseerimist.</p>
            <p>See valmis autori bakalaureusetöö tulemusena.</p>
        </div>

        <div class="links">
        <Button icon="pi pi-fw pi-cog" label="Try Facedescriber" @click="this.$router.push('/face-describer')" class = "EN"/>
        <Button icon="pi pi-fw pi-cog" label="Proovi Facedescriberit" @click="this.$router.push('/face-describer')" class = "EE"/>
        <a href = "https://github.com/KarlMagnusLaikoja/face-describer" target="_blank">
                <Button icon="pi pi-github" label="See the source code" class = "EN"/>
                <Button icon="pi pi-github" label="Vaata lähtekoodi" class = "EE"/>
        </a>
        </div>
    </div>
    <Divider/>
    <div class="homepage_description EN" v-if="this.$store.state.languageCode=='EN'">
        <description v-for="image in images" :key="image" :value="image" ref="images" v-bind:image="image"/>
    </div>
    <div class="homepage_description EE" v-if="this.$store.state.languageCode=='EE'">
        <description v-for="image in images" :key="image" :value="image" ref="images" v-bind:image="image"/>
    </div>
    <Divider/>
    <div class="faq">
            <h1 class="EN">What does Facedescriber do?</h1>
            <h1 class="EE">Mida teeb Facedescriber?</h1>
            <Accordion multiple="true" :activeIndex="0" class="algorithmSteps">
                <AccordionTab>
                    <template #header>
                                    <span class="font-bold white-space-nowrap EN">1. Finds various facial landmarks within the input image</span>
                                    <span class="font-bold white-space-nowrap EE">1. Leiab sisendpildilt erinevad näomarkerid</span>
                    </template>
                    <p class="EN">
                        The <a href = "https://pypi.org/project/face-recognition/" target="_blank">face-recognition</a> module is used to verify that there is a face within
                        the image. Then it is used to find the coordinates of different facial landmarks (such as the eyes, nose, chin), which are used to crop the image into subimages
                        to be used in further analysis.
                    </p>
                    <p class="EE">
                    Kontrollimaks, et pildil on nägu, kasutatakse <a href = "https://pypi.org/project/face-recognition/" target="_blank">face-recognition</a> moodulit.
                    Seejärel leitakse selle abil iga näomarkeri (näiteks silmad, nina, lõug) koordinaadid, mida kasutatakse pildi pügamiseks alampiltideks edasise analüüsi jaoks.
                    </p>
                </AccordionTab>
                <AccordionTab>
                    <template #header>
                                    <span class="font-bold white-space-nowrap EN">2. Applies image processing techniques and classification functions to each landmark</span>
                                    <span class="font-bold white-space-nowrap EE">2. Rakendab pilditöötlusvõtteid ja klassifitseerimisfunktsioone igale alampildile</span>
                    </template>
                    <p class="EN">
                    Each subimage goes through specialized image processing and classification, comparing those landmarks to "standard" landmarks. For example, in the case
                    of eye colour, the RGB values of each eye are compared to specially picked examples of different eye colours and the colour of the eye is classified based on the closest match.
                    </p>
                    <p class="EE">
                    Iga alampilt läbib kohandatud pilditöötluse ja klassifitseerimise, mis võrdleb pildil olevat markerit nii-öelda "standardmarkeritega". Näiteks silmavärvi puhul
                    võrreldakse kummagi silma RGB väärtusi spetsiaalselt valitud näidete vastu erinevatest silmavärvidest ning silmavärv klassifitseeritakse lähima väärtuse põhjal.
                    </p>
                </AccordionTab>
                <AccordionTab>
                    <template #header>
                                    <span class="font-bold white-space-nowrap EN">3. Compiles the results</span>
                                    <span class="font-bold white-space-nowrap EE">3. Paneb kokku kirjelduse</span>
                    </template>
                    <p class="EN">
                    The results of each subimage's analysis are compiled into a single, full description.
                    </p>
                    <p class="EE">
                    Iga alampildi analüüsi tulemused kompileeritakse üheks tervikuks kirjelduseks.
                    </p>
                </AccordionTab>
            </Accordion>
    </div>
</div>
</template>

<script>
import {renderLanguage} from './AppHeader.vue';
import Description from './Description.vue';
export default {
  name: 'HomePage',
  components: {
        Description
  },
  created () {
      //Get specific image from gallery
      const galleryFiles = require.context('../assets/gallery', false)
                                  .keys().map(key => key.slice(2)).filter((file) => file == "homepage.png")
      this.images.push(galleryFiles[0]);
  },
  mounted () {
    renderLanguage(this.$store.state.languageCode);
  },
     data() {
               return {
                   images: [],
               }
           }
}
</script>