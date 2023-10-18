<template>
    <h1>{{msg}}</h1>
</template>

<script>
export default {
  name: 'DescriptionComponent',
    data() {
        return {
            msg: ''
        }
    },
    mounted(){
        fetch("/describe")
            .then((response) => response.text())
            .then((data) => {
            this.msg = data;
            })
    }
}
</script>

