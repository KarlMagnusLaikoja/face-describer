<template>
<div class="home">
    <div class="intro">
        <p>intro</p>
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
            <h1 class="EN">What does Face-Describer do?</h1>
            <h1 class="EE">Mida teeb Face-Describer?</h1>
            <Accordion multiple="true" :activeIndex="0" class="algorithmSteps">
                <AccordionTab>
                    <template #header>
                                    <span class="font-bold white-space-nowrap EN">1. Finds various facial landmarks within the input image</span>
                                    <span class="font-bold white-space-nowrap EE">1. Leiab sisendpildilt erinevad näomarkerid</span>
                    </template>
                    <p class="EN">
                        The <a href = "https://pypi.org/project/face-recognition/" target="_blank">face-recognition</a> module is used to verify that there is a face within
                        the image. Then it is used to find the coordinates of different facial landmarks (such as the eyes, nose, chin), which are used to crop the image into subimages
                        to be used in analysis.
                    </p>
                    <p class="EE">
                    Kontrollimaks, et pildil on nägu, kasutatakse <a href = "https://pypi.org/project/face-recognition/" target="_blank">face-recognition</a> moodulit.
                    Seejärel leitakse selle abil iga näomarkeri (näiteks silmad, nina, lõug) koordinaadid, mida kasutatakse pildi pügamiseks alampiltideks edasise analüüsi jaoks.
                    </p>
                </AccordionTab>
                <AccordionTab>
                    <template #header>
                                    <span class="font-bold white-space-nowrap EN">2. Applies image processing to each landmark</span>
                                    <span class="font-bold white-space-nowrap EE">2. Rakendab pilditöötlusvõtteid igale alampildile</span>
                    </template>
                    <p class="EN">
                    Each subimage goes through specialized image processing, comparing those landmarks to "standard" landmarks. For example, in the case
                    of eye colour, the RGB values of each eye are compared to specially picked examples of different eye colours.
                    </p>
                    <p class="EE">
                    Iga alampilt läbib kohandatud pilditöötluse, mis võrdleb pildil olevat markerit nii-öelda "standardmarkeritega". Näiteks silmavärvi puhul
                    võrreldakse kummagi silma RGB väärtusi spetsiaalselt valitud näidete vastu erinevatest silmavärvidest.
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
import Description from './Description.vue'
export default {
  name: 'HomePage',
  components: {
        Description
  },
  created () {
      //Get first image from gallery
      const galleryFiles = require.context('../assets/gallery', false)
                                  .keys().map(key => key.slice(2))
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