class Mls < Formula
  desc "Terminal-native audio/video/image file browser with TUI preview and JSON output"
  homepage "https://github.com/thepushkarp/mls"
  version "0.0.3"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/thepushkarp/mls/releases/download/v#{version}/mls-v#{version}-aarch64-apple-darwin.tar.gz"
      sha256 "92ca53dce212f3cd9741db216054f604ecd51e3987eec038cdd152ff15487b50"
    elsif Hardware::CPU.intel?
      url "https://github.com/thepushkarp/mls/releases/download/v#{version}/mls-v#{version}-x86_64-apple-darwin.tar.gz"
      sha256 "2566bbce34f19a03fecf79b2f46c89c58205a0336d77d6767f205206de986815"
    end
  end

  depends_on :macos
  depends_on "ffmpeg"
  depends_on "mpv"

  def install
    bin.install "mls"
  end

  test do
    assert_match "Media LS", shell_output("#{bin}/mls --help")
  end
end
