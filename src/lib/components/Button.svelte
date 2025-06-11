<script lang='ts'>
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome'
    import { config } from '@fortawesome/fontawesome-svg-core'

    import '@fortawesome/fontawesome-svg-core/styles.css' // Import the CSS
    config.autoAddCss = false // Tell Font Awesome to skip adding the CSS automatically since it's being imported above

    type Props = { // args from parent
        icon: any
        large?: boolean
        onclick: MouseEvent
    }
    const { icon, large, onclick }: Props = $props()
</script>

<button {onclick}
    class={["rounded-full bg-gray-400 p-0.5 size-10", large ? "scale-150" : ""]}>
    <FontAwesomeIcon {icon}/>
</button>
