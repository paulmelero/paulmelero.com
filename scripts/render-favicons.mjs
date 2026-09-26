import { readFileSync, writeFileSync } from 'node:fs'
import { Resvg } from '@resvg/resvg-js'

const svg = readFileSync(new URL('../public/favicon.svg', import.meta.url))

const render = (size) =>
  new Resvg(svg, { fitTo: { mode: 'width', value: size } }).render().asPng()

const png = (size) => {
  const data = render(size)
  writeFileSync(new URL(`../public/favicon-${size}x${size}.png`, import.meta.url), data)
  return data
}

const sizes = [16, 32]
const images = sizes.map((size) => ({ size, data: png(size) }))
writeFileSync(new URL('../public/apple-touch-icon.png', import.meta.url), render(180))

const header = Buffer.alloc(6)
header.writeUInt16LE(0, 0)
header.writeUInt16LE(1, 2)
header.writeUInt16LE(images.length, 4)

let offset = 6 + images.length * 16
const entries = images.map(({ size, data }) => {
  const entry = Buffer.alloc(16)
  entry.writeUInt8(size, 0)
  entry.writeUInt8(size, 1)
  entry.writeUInt16LE(1, 4)
  entry.writeUInt16LE(32, 6)
  entry.writeUInt32LE(data.length, 8)
  entry.writeUInt32LE(offset, 12)
  offset += data.length
  return entry
})

writeFileSync(
  new URL('../public/favicon.ico', import.meta.url),
  Buffer.concat([header, ...entries, ...images.map(({ data }) => data)]),
)

console.log(`favicons rendered: ${sizes.join(', ')}px ico + 180px apple-touch-icon`)